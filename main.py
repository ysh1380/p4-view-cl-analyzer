#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Perforce client template의 View 매핑을 한 줄씩 읽어서,
각 경로에 대해 [start_cl ~ end_cl] 사이 changelist 목록을
번호 + 사용자 + 날짜 + 설명(첫 줄) 과 함께 출력

사용 예시:
    python3 main.py 1500000 1505000
    python3 main.py 1234000 1238000 --template 애플_C --short-desc
"""

import subprocess
import sys
import argparse
import re


def run_p4(cmd_list, input_text=None, check=True):
    """p4 명령어 실행 헬퍼"""
    try:
        result = subprocess.run(
            ["p4"] + cmd_list,
            input=input_text,
            text=True,
            check=check,
            capture_output=True,
            encoding="utf-8"
        )
        return result.stdout.strip()
    except FileNotFoundError:
        print("오류: 시스템에서 'p4' 명령어를 찾을 수 없습니다. Perforce 클라이언트가 설치되어 있고 PATH에 등록되어 있는지 확인해 주세요.", file=sys.stderr)
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        if not check:
            return ""
        print("p4 오류:", file=sys.stderr)
        print("  명령어:", " ".join(["p4"] + cmd_list), file=sys.stderr)
        print("  에러:", e.stderr.strip(), file=sys.stderr)
        sys.exit(1)


def get_template_view_lines(template_name="애플_C"):
    """템플릿 spec에서 View: 매핑 경로들만 추출 (depot 쪽 경로)"""
    spec = run_p4(["client", "-t", template_name, "-o"])
    lines = spec.splitlines()

    view_paths = []
    in_view = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("View:"):
            in_view = True
            continue
        if in_view:
            if not stripped or stripped.startswith(("#", "Options:", "Root:", "Stream:")):
                break
            # depot 경로 추출 (//depot/... 부분)
            parts = re.split(r'\s+', stripped)
            if parts and parts[0].startswith("//"):
                path = parts[0].rstrip("/...")
                view_paths.append(path + "/...")

    return view_paths


def get_changes_with_desc(depot_path, start_cl, end_cl):
    """p4 changes -l 로 설명 포함 목록 가져오기"""
    cmd = [
        "changes",
        "-l",                # 긴 설명 포함
        "-s", "submitted",
        f"{depot_path}@{start_cl},{end_cl}"
    ]
    output = run_p4(cmd, check=False)

    changes = []
    current = None

    for line in output.splitlines():
        if line.startswith("Change "):
            if current:
                changes.append(current)
            parts = line.split()
            try:
                cl = int(parts[1])
                by_user = parts[3].rstrip("'")
                on_date = " ".join(parts[5:9])   # 날짜+시간 부분 대략
                current = {"cl": cl, "user": by_user, "date": on_date, "desc": ""}
            except:
                current = None
        elif current and line.strip():
            # 설명 첫 줄만 저장 (또는 전체 원하면 current["desc"] += line + "\n")
            if not current["desc"]:
                current["desc"] = line.strip()

    if current:
        changes.append(current)

    return sorted(changes, key=lambda x: x["cl"])


def main():
    parser = argparse.ArgumentParser(description="View별 범위 내 CL 목록 + 설명 출력")
    parser.add_argument("start_cl", type=int, help="시작 CL (포함)")
    parser.add_argument("end_cl",   type=int, help="끝   CL (포함)")
    parser.add_argument("--template", default="애플_C", help="client template 이름")
    parser.add_argument("--short-desc", action="store_true",
                        help="설명 첫 60자 정도로 짧게 자르기")
    parser.add_argument("--min-cl", type=int, default=1,
                        help="CL 개수가 이 이상일 때만 출력 (기본 1)")

    args = parser.parse_args()

    if args.start_cl >= args.end_cl:
        print("오류: 시작 CL >= 끝 CL", file=sys.stderr)
        sys.exit(1)

    print(f"템플릿     : {args.template}")
    print(f"범위       : {args.start_cl} ~ {args.end_cl}")
    print(f"최소 CL 수 : {args.min_cl}\n")

    paths = get_template_view_lines(args.template)

    if not paths:
        print("View 경로를 찾을 수 없습니다. 템플릿 이름을 확인해 주세요.")
        sys.exit(1)

    print(f"발견된 View 경로 수: {len(paths)}\n")

    for i, path in enumerate(paths, 1):
        print(f"[{i:2d}] {path}")

        changes = get_changes_with_desc(path, args.start_cl, args.end_cl)

        count = len(changes)
        if count < args.min_cl:
            if count > 0:
                print(f"    → {count}개 (최소 기준 미달, 스킵)")
            else:
                print("    → 범위 내 변경사항 없음")
            print()
            continue

        print(f"    → 포함된 CL: {count}개")

        for ch in changes:
            desc = ch["desc"]
            if args.short_desc:
                desc = (desc[:57] + "...") if len(desc) > 60 else desc

            print(f"      {ch['cl']:>7}  {ch['user']:<12}  {ch['date']:<19}  {desc}")

        print()


if __name__ == "__main__":
    main()
