# Jarvis Office Colony (Command-Driven UX Critic Edition)

요청사항에 맞춰 에이전트를 **불만 + 조시** 2명으로 운영하며, **사용자 명령이 들어오면** 불만이 고강도 비평을 수행하고 조시가 즉시 수정합니다.

## 핵심 규칙
- 에이전트는 **업무가 없는(unassigned) 상태** 기반
- `불만`: 명령 수신 시 무조건 강하게 문제점을 탐색하고 조시에게 수정 지시
- `조시`: 불만의 지시를 계속 듣고 UX/UI를 반복 수정
- 매 라운드마다 둘 다 최신 모델로 업데이트(지속 조사/학습)
- 인사 모드에서는 둘 다 기립 상태로 `안녕하세요 / Hello`

## 파일 구조
- `src/office_simulation.py`: 명령기반 비평/수정/최신모델 업데이트 코어
- `main.py`: CLI 데모
- `config/agents.yaml`: 정책/에이전트 규칙
- `web/index.html`: 오피스풍 인터랙티브 UI

## CLI 실행
```bash
python3 main.py
```

## 웹 UI 실행
```bash
python3 -m http.server 8000
# http://localhost:8000/web/index.html
```

## 웹 UI 기능
- 사용자 명령 입력 후 `Command Bulman` 실행
- 불만의 강한 문제 제기 → 조시 즉시 수정 루프
- 라운드마다 `ui_version`, `ux_quality` 증가
- 두 에이전트의 `model_rev`와 `learning` 지속 증가
