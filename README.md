# Jarvis Office Colony (Skeleton)

림월드 감성의 6인 에이전트 오피스 시뮬레이션입니다.

## 핵심 목표
- 도메인: 투자 / 코인 / 밈코인
- 규율: 업무 중에만 착석, 대기 시 기립/이동
- 보고 체계: 일반 에이전트 → 팀장(보운) → 사용자
- 전원 이중언어: 한국어/영어 (ko/en)

## 팀 구조
- 팀장: **보운** (`agent_01`)
- 전문 에이전트: **리모** (`agent_02`, crypto/memecoin)
- SOTA 프레임워크 소유: 보운/리모
- 보운/리모가 프레임워크를 다른 에이전트에게 전파 가능

## SOTA 지식 메모리
내장 키: `sota_expectation_engine_v3_3`

가능 동작:
1. 보운/리모 학습
2. 즉시 회상(recall)
3. 팀 전체 전파(teach-to-peer)
4. 시장 업데이트 루프와 결합

## 폴더 구조
- `config/agents.yaml`: 팀/거버넌스/지식 소유 설정
- `src/office_simulation.py`: 시뮬레이션 코어
- `main.py`: CLI 데모
- `web/index.html`: 고퀄 오피스형 시각 UI

## 실행
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python main.py
```

## 웹 UI 실행
```bash
python3 -m http.server 8000
# http://localhost:8000/web/index.html
```

## UI 기능
- 림월드 스타일 캐릭터 이동 + 실제 사무실 느낌의 공간 구성
- 업무/브리핑/대기/성장/인사 모드
- 전원 기립 인사(안녕하세요 / Hello)
- 팀 상태/언어/지식 상태 가시화


## MiroFish 적용 상태
- 원본 레포: `https://github.com/666ghj/MiroFish.git`
- 현재 환경 네트워크 제한(403)으로 직접 clone 불가
- 대체 적용: `mirofish_fallback_playbook`
  - swarm scan -> lead filter -> synchronized execution -> feedback learning
- 보운/리모가 우선 로드 후 팀 전체 전파 가능
