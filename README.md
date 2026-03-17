# Jarvis Office Colony (UX Critic Loop Edition)

요청사항에 맞춰 에이전트 구성을 **불만 + 조시** 2명으로 재구성했습니다.

## 핵심 규칙
- 에이전트는 **업무가 없는(unassigned) 상태** 기반으로 동작
- `불만`: UX 사용자 관점에서 **항상 부정적 비평**, **절대 칭찬 금지**
- `조시`: 불만의 피드백을 계속 듣고 UX/UI를 반복 수정
- 두 에이전트는 라운드형 대화를 통해 지속적으로 성장
- 인사 모드에서는 둘 다 기립 상태로 `안녕하세요 / Hello`

## 파일 구조
- `src/office_simulation.py`: 불만-조시 대화형 UX 개선 코어
- `main.py`: CLI 데모 실행
- `config/agents.yaml`: 정책/에이전트 설정
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
- 게임풍 사무실 내부에서 2명 캐릭터가 자유 이동
- `UX Critic Loop` 버튼으로 불만↔조시 반복 대화 실행
- 라운드별 비평/개선 로그 출력
- `ui_version`, `ux_quality` 실시간 갱신
