# p4-view-cl-analyzer

Perforce (Helix Core) client template의 View 매핑을 한 줄씩 분석해서,  
**특정 CL 범위(start ~ end)** 안에 포함된 changelist 목록을 경로별로 출력해주는 도구입니다.

- View가 수십~수백 개여도 한 번에 처리
- 각 CL의 번호 + 작성자 + 날짜 + 설명(첫 줄)까지 보여줌
- 대규모 프로젝트에서 "이 범위에서 어떤 변경이 있었나?" 빠르게 확인할 때 유용

## 옵션

- `--template NAME`: Perforce client template 이름 (기본값: `Common_Release`)
- `--short-desc`: 설명을 약 60자 정도로 절삭하여 출력
- `--min-cl N`: CL 개수가 N개 미만이면 해당 경로 스킵 (노이즈 제거용)

## 사용법

```bash
# 기본 사용
python main.py 1500000 1505000

# 옵션 사용 (설명 절삭 + 5개 이상 경로)
python main.py 1234000 1240000 --short-desc --min-cl 5

# 템플릿 지정
python main.py 2000000 2010000 --template 애플_C_release
```

## 출력 예시

```text
템플릿     : Common_Release
범위       : 1500000 ~ 1505000
최소 CL 수 : 1

발견된 View 경로 수: 2

[ 1] //depot/product/xxx/...
    → 포함된 CL: 2개
      1500123  dev.kim       2026/02/28 14:35:22  [UI] 버튼 색상 피드백 반영
      1500156  tester.park    2026/03/01 09:12:45  린트 에러 전체 수정

[ 2] //depot/asset/character/...
    → 범위 내 변경사항 없음
```

## 프로젝트 구조
- `main.py`: 핵심 분석 스크립트
- `requirements.txt`: 필요한 라이브러리 목록
- `LICENSE`: MIT 라이선스
- `.gitignore`: Git 관리 제외 설정
