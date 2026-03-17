from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Agent:
    agent_id: str
    name: str
    role: str
    persona: str
    languages: List[str] = field(default_factory=lambda: ["ko", "en"])
    is_working: bool = False
    is_seated: bool = False
    learning_score: float = 1.0
    dialogue_count: int = 0
    memory: Dict[str, str] = field(default_factory=dict)

    def greeting(self) -> str:
        return f"[{self.agent_id}] {self.name}: 안녕하세요! Hello!"


@dataclass
class OfficeSimulation:
    agents: List[Agent] = field(default_factory=list)
    user_name: str = "YOU"
    ui_version: int = 1
    ux_quality_score: float = 40.0

    def _critic(self) -> Agent:
        for agent in self.agents:
            if agent.name == "불만":
                return agent
        raise ValueError("Critic '불만' not found")

    def _fixer(self) -> Agent:
        for agent in self.agents:
            if agent.name == "조시":
                return agent
        raise ValueError("Fixer '조시' not found")

    def run_team_greeting(self) -> List[str]:
        return [agent.greeting() for agent in self.agents]

    def run_ux_improvement_cycle(self, rounds: int = 3) -> List[str]:
        critic = self._critic()
        fixer = self._fixer()
        logs: List[str] = []

        for round_no in range(1, rounds + 1):
            critic.dialogue_count += 1
            fixer.dialogue_count += 1

            issue = self._generate_negative_feedback(round_no)
            logs.append(f"[ROUND {round_no}] [{critic.name}] {issue}")

            action = self._generate_fix_action(round_no)
            self.ui_version += 1
            self.ux_quality_score = round(min(95.0, self.ux_quality_score + 7.5), 1)
            logs.append(
                f"[ROUND {round_no}] [{fixer.name}] {action} | ui_version=v{self.ui_version} | ux_quality={self.ux_quality_score}"
            )

            critic.learning_score = round(critic.learning_score + 0.06, 2)
            fixer.learning_score = round(fixer.learning_score + 0.09, 2)

        critic.memory["ux_critic_mode"] = "always_negative_never_praise"
        fixer.memory["ux_fix_strategy"] = "listen_to_bulman_and_iterate"
        logs.append(
            f"[REPORT] {fixer.name} -> {self.user_name}: 불만 피드백 기반 UX/UI 개선 루프 완료 (총 {rounds}회)."
        )
        return logs

    def _generate_negative_feedback(self, round_no: int) -> str:
        feedback_pool = [
            "문제: 정보 위계가 약해서 사용자가 핵심 액션을 즉시 파악하지 못합니다.",
            "문제: 시선 흐름이 분산되어 첫 3초 내 목적지향적 탐색에 실패합니다.",
            "문제: 상태 변화 피드백이 부족해 상호작용 결과를 신뢰하기 어렵습니다.",
            "문제: 대비와 간격 체계가 불완전해 인지 부하가 높습니다.",
        ]
        return feedback_pool[(round_no - 1) % len(feedback_pool)]

    def _generate_fix_action(self, round_no: int) -> str:
        action_pool = [
            "조치: 좌측 패널을 핵심 우선순위 구조로 재배치하고 CTA를 상단 고정했습니다.",
            "조치: 캐릭터 상태 링과 작업 버블의 시각적 대비를 확대했습니다.",
            "조치: 버튼 반응/로그 타임스탬프를 추가해 행동-결과 연결성을 강화했습니다.",
            "조치: 레이아웃 그리드와 타이포 스케일을 재정렬해 가독성을 개선했습니다.",
        ]
        return action_pool[(round_no - 1) % len(action_pool)]


def build_default_agents() -> List[Agent]:
    return [
        Agent(
            agent_id="agent_01",
            name="불만",
            role="Unassigned Agent / Senior UX Critic",
            persona="always-negative, never-praise, expert-level",
        ),
        Agent(
            agent_id="agent_02",
            name="조시",
            role="Unassigned Agent / UX UI Fixer",
            persona="listener-implementer, iterative-improvement",
        ),
    ]
