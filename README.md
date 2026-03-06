# p4-view-cl-analyzer

Perforce (Helix Core) client template의 View 매핑을 한 줄씩 분석해서,  
**특정 CL 범위(start ~ end)** 안에 포함된 changelist 목록을 경로별로 출력해주는 도구입니다.

- View가 수십~수백 개여도 한 번에 처리
- 각 CL의 번호 + 작성자 + 날짜 + 설명(첫 줄)까지 보여줌
- 대규모 프로젝트에서 "이 범위에서 어떤 변경이 있었나?" 빠르게 확인할 때 유용

## 주요 기능

## 옵션

- `--template NAME`: Perforce client template 이름 (기본값: `Common_Release`)
- `--short-desc`: 설명을 약 60자 정도로 잘라서 출력
- `--min-cl N`: CL 개수가 N개 미만이면 해당 경로 스킵 (노이즈 제거용)

## 사용법

```bash
# 기본 사용 (시작 CL ~ 종료 CL, 템플릿 기본값 'Common_Release' 사용)
python main.py 1500000 1505000

# 설명 짧게 자르기 + 최소 5개 이상인 경로만 보기
python main.py 1234000 1240000 --short-desc --min-cl 5

# 다른 템플릿 이름 지정
python main.py 2000000 2010000 --template 애플_C_release
```

## 프로젝트 구조
- `main.py`: 핵심 분석 스크립트
- `requirements.txt`: 필요한 라이브러리 목록
- `LICENSE`: MIT 라이선스
- `.gitignore`: Git 관리 제외 설정
