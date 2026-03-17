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
    latest_model_revision: int = 1
    memory: Dict[str, str] = field(default_factory=dict)

    def greeting(self) -> str:
        return f"[{self.agent_id}] {self.name}: 안녕하세요! Hello!"

    def update_to_latest_model(self) -> str:
        self.latest_model_revision += 1
        self.learning_score = round(min(10.0, self.learning_score + 0.11), 2)
        return (
            f"[{self.agent_id}] {self.name} 최신 모델 업데이트 완료 "
            f"(model_rev=r{self.latest_model_revision}, learning={self.learning_score})."
        )


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

    def run_user_commanded_ux_loop(self, command: str, rounds: int = 3) -> List[str]:
        critic = self._critic()
        fixer = self._fixer()
        logs: List[str] = []

        logs.append(f"[COMMAND] {self.user_name}: {command}")
        logs.append(f"[ACK] {critic.name}: 명령 수신. 즉시 고강도 문제 탐색 시작.")

        for round_no in range(1, rounds + 1):
            critic.dialogue_count += 1
            fixer.dialogue_count += 1

            issue = self._generate_hard_negative_feedback(round_no)
            logs.append(f"[ROUND {round_no}] [{critic.name}] {issue}")
            logs.append(f"[ROUND {round_no}] [{critic.name} -> {fixer.name}] 지금 바로 수정해.")

            action = self._generate_fix_action(round_no)
            self.ui_version += 1
            self.ux_quality_score = round(min(98.0, self.ux_quality_score + 8.0), 1)
            logs.append(
                f"[ROUND {round_no}] [{fixer.name}] {action} | ui_version=v{self.ui_version} | ux_quality={self.ux_quality_score}"
            )

            logs.append(critic.update_to_latest_model())
            logs.append(fixer.update_to_latest_model())

        critic.memory["critic_mode"] = "always_negative_extreme_issue_hunt"
        fixer.memory["fix_mode"] = "bulman_feedback_first"
        logs.append(
            f"[REPORT] {fixer.name} -> {self.user_name}: 불만의 비평을 모두 반영해 UX/UI 개선 완료. "
            f"두 에이전트 최신 모델 동기화 유지 중."
        )
        return logs

    def _generate_hard_negative_feedback(self, round_no: int) -> str:
        feedback_pool = [
            "치명적 문제: 정보 구조가 사용자 목표 흐름을 방해합니다. 현재 상태는 실사용 기준 실패입니다.",
            "치명적 문제: 핵심 인터랙션의 피드백 밀도가 낮아 오작동으로 오해될 수준입니다.",
            "치명적 문제: 시각 계층과 대비 설계가 일관되지 않아 인지 비용이 과도합니다.",
            "치명적 문제: 행동 우선순위가 흐려 첫 5초 내 올바른 액션 유도가 불가능합니다.",
        ]
        return feedback_pool[(round_no - 1) % len(feedback_pool)]

    def _generate_fix_action(self, round_no: int) -> str:
        action_pool = [
            "조치: 정보 위계를 재설계하고 핵심 CTA를 상단 고정하여 목표 경로를 단일화했습니다.",
            "조치: 인터랙션 성공/실패 상태 피드백을 즉시 표시하도록 반응 체계를 확장했습니다.",
            "조치: 타이포/간격/컬러 대비 토큰을 표준화해 시각 일관성을 재정립했습니다.",
            "조치: 첫 화면 행동 유도 요소를 재배치해 5초 내 진입 성공률을 강화했습니다.",
        ]
        return action_pool[(round_no - 1) % len(action_pool)]


def build_default_agents() -> List[Agent]:
    return [
        Agent(
            agent_id="agent_01",
            name="불만",
            role="Unassigned Agent / Senior UX Critic",
            persona="always-negative, command-driven issue hunter",
        ),
        Agent(
            agent_id="agent_02",
            name="조시",
            role="Unassigned Agent / UX UI Fixer",
            persona="feedback-first rapid fixer",
        ),
    ]
