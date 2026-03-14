from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Task:
    title: str
    category: str  # investment | coin | memecoin
    priority: int = 1
    important: bool = False
    requires_approval: bool = False


@dataclass
class Agent:
    agent_id: str
    name: str
    role: str
    personality: str
    creativity_style: str
    growth_goal: str
    expertise: List[str] = field(default_factory=list)
    reports_to: Optional[str] = None
    is_team_lead: bool = False
    is_working: bool = False
    is_seated: bool = False
    completed_tasks: int = 0
    knowledge_score: float = 1.0

    def start_task(self, task: Task) -> str:
        self.is_working = True
        self.is_seated = True
        self.completed_tasks += 1
        return f"[{self.agent_id}] {self.name} starts '{task.title}' ({task.category}) while seated at desk."

    def stop_task(self) -> str:
        self.is_working = False
        self.is_seated = False
        return f"[{self.agent_id}] {self.name} is now idle and standing."

    def update_from_best_sources(self) -> str:
        self.knowledge_score = round(self.knowledge_score + 0.1, 2)
        return (
            f"[{self.agent_id}] {self.name} updates from top-tier sources "
            f"and improves knowledge score to {self.knowledge_score}."
        )

    def share_insight(self, peer: "Agent") -> str:
        return (
            f"[{self.agent_id}] {self.name} shares {', '.join(self.expertise)} insight with "
            f"[{peer.agent_id}] {peer.name}."
        )

    def evolve(self) -> str:
        self.knowledge_score = round(self.knowledge_score + 0.05, 2)
        return (
            f"[{self.agent_id}] {self.name} evolves: refining strategy for '{self.growth_goal}' "
            f"(knowledge={self.knowledge_score})."
        )


@dataclass
class OfficeSimulation:
    agents: List[Agent] = field(default_factory=list)
    user_name: str = "Owner"

    def _agent_map(self) -> Dict[str, Agent]:
        return {agent.agent_id: agent for agent in self.agents}

    def _team_lead(self) -> Agent:
        for agent in self.agents:
            if agent.is_team_lead:
                return agent
        raise ValueError("No team lead configured.")

    def assign_tasks(self, tasks: List[Task]) -> List[str]:
        logs: List[str] = []
        if not tasks:
            logs.extend(self.set_idle_mode())
            return logs

        ordered = sorted(tasks, key=lambda t: t.priority, reverse=True)
        for idx, task in enumerate(ordered):
            assignee = self.agents[idx % len(self.agents)]
            logs.append(assignee.start_task(task))
            if task.important or task.requires_approval:
                logs.extend(self._report_chain_for_task(assignee, task))

        return logs

    def _report_chain_for_task(self, assignee: Agent, task: Task) -> List[str]:
        logs: List[str] = []
        lead = self._team_lead()

        if assignee.agent_id != lead.agent_id:
            logs.append(
                f"[{assignee.agent_id}] {assignee.name} reports IMPORTANT '{task.title}' to "
                f"team lead [{lead.agent_id}] {lead.name}."
            )

        logs.append(
            f"[{lead.agent_id}] {lead.name} reviews/filters the report and escalates to "
            f"{self.user_name}."
        )

        if task.requires_approval:
            logs.append(
                f"[APPROVAL FLOW] agent -> team lead({lead.name}) -> {self.user_name} required for '{task.title}'."
            )

        return logs

    def run_peer_dialogue_cycle(self) -> List[str]:
        logs: List[str] = []
        if len(self.agents) < 2:
            return logs

        for idx, speaker in enumerate(self.agents):
            listener = self.agents[(idx + 1) % len(self.agents)]
            logs.append(speaker.share_insight(listener))

        return logs

    def run_market_intel_cycle(self) -> List[str]:
        logs: List[str] = []
        lead = self._team_lead()

        for agent in self.agents:
            logs.append(agent.update_from_best_sources())

            # 리모: 밈코인/크립토 전문 최신 정보 수집 -> 팀장 보고
            if agent.name == "리모":
                logs.append(
                    f"[{agent.agent_id}] 리모 submits curated memecoin/crypto opportunities to "
                    f"team lead [{lead.agent_id}] {lead.name}."
                )
                logs.append(
                    f"[{lead.agent_id}] {lead.name} filters Rimo's intel and reports key points to {self.user_name}."
                )

        return logs

    def set_idle_mode(self) -> List[str]:
        logs: List[str] = []
        for agent in self.agents:
            if agent.is_working or agent.is_seated:
                logs.append(agent.stop_task())
        return logs

    def run_growth_cycle(self) -> List[str]:
        return [agent.evolve() for agent in self.agents]


def build_default_agents() -> List[Agent]:
    return [
        Agent(
            agent_id="agent_01",
            name="보운",
            role="Team Lead / Chief Strategist",
            personality="calm-decisive",
            creativity_style="structured synthesis",
            growth_goal="maximize team quality and decision reliability",
            expertise=["investment", "portfolio", "risk"],
            is_team_lead=True,
        ),
        Agent(
            agent_id="agent_02",
            name="리모",
            role="Crypto & Memecoin Specialist",
            personality="fast-scout",
            creativity_style="trend hunting",
            growth_goal="track real-time crypto/memecoin alpha",
            expertise=["coin", "memecoin", "onchain"],
            reports_to="agent_01",
        ),
        Agent(
            agent_id="agent_03",
            name="TBD-3",
            role="Macro Analyst",
            personality="evidence-driven",
            creativity_style="scenario planning",
            growth_goal="connect macro signals to coin strategy",
            expertise=["investment", "macro"],
            reports_to="agent_01",
        ),
        Agent(
            agent_id="agent_04",
            name="TBD-4",
            role="Risk Controller",
            personality="strict",
            creativity_style="constraint optimization",
            growth_goal="reduce drawdown and approval errors",
            expertise=["risk", "compliance"],
            reports_to="agent_01",
        ),
        Agent(
            agent_id="agent_05",
            name="TBD-5",
            role="Execution Operator",
            personality="pragmatic",
            creativity_style="rapid iteration",
            growth_goal="improve execution speed and consistency",
            expertise=["execution", "ops"],
            reports_to="agent_01",
        ),
        Agent(
            agent_id="agent_06",
            name="TBD-6",
            role="Research Synthesizer",
            personality="curious",
            creativity_style="cross-domain synthesis",
            growth_goal="merge scattered intel into clear action",
            expertise=["research", "synthesis"],
            reports_to="agent_01",
        ),
    ]
