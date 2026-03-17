from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional




MIROFISH_FALLBACK_PLAYBOOK = """MiroFish-style fallback playbook (network-restricted):
1) swarm scan -> 2) lead filter -> 3) synchronized execution -> 4) feedback learning
"""

SOTA_EXPECTATION_ENGINE_V3_3 = """■ SOTA Expectation-Driven Valuation Engine v3.3
■ High-Beta / Optionality / Product-Platform Hybrid Edition
핵심요약:
- DCF는 메인 엔진이 아닌 cross-check
- Intrinsic = Core + Execution + Ecosystem - Drag
- 중요/승인 흐름: agent -> 팀장 -> 사용자
- Product-Platform Hybrid는 pure manufacturing multiple 금지
- Scenario 확률 규칙 강제(Bear/Base/Bull Execution/Bull Ecosystem)
- 보고서는 숫자 중심, 데이터 태그([실제]/[추정]/[가정]) 엄수
"""


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
    languages: List[str] = field(default_factory=lambda: ["ko", "en"])
    reports_to: Optional[str] = None
    is_team_lead: bool = False
    is_working: bool = False
    is_seated: bool = False
    completed_tasks: int = 0
    knowledge_score: float = 1.0
    knowledge_base: Dict[str, str] = field(default_factory=dict)
    swarm_role: str = "scout"
    signal_confidence: float = 0.5

    def start_task(self, task: Task) -> str:
        self.is_working = True
        self.is_seated = True
        self.completed_tasks += 1
        return f"[{self.agent_id}] {self.name} starts '{task.title}' ({task.category}) while seated at desk."

    def stop_task(self) -> str:
        self.is_working = False
        self.is_seated = False
        return f"[{self.agent_id}] {self.name} is now idle and standing."

    def greeting(self) -> str:
        return f"[{self.agent_id}] {self.name}: 안녕하세요! Hello!"

    def apply_mirofish_playbook(self) -> str:
        self.knowledge_base["mirofish_playbook"] = MIROFISH_FALLBACK_PLAYBOOK
        self.signal_confidence = round(min(1.0, self.signal_confidence + 0.1), 2)
        return f"[{self.agent_id}] {self.name} loaded MiroFish fallback playbook (confidence={self.signal_confidence})."


    def learn_framework(self, key: str, content: str) -> str:
        self.knowledge_base[key] = content
        self.knowledge_score = round(self.knowledge_score + 0.08, 2)
        return f"[{self.agent_id}] {self.name} learned framework '{key}'."

    def recall_framework(self, key: str) -> str:
        if key not in self.knowledge_base:
            return f"[{self.agent_id}] {self.name} cannot recall '{key}' yet."
        return f"[{self.agent_id}] {self.name} recalls '{key}' and is ready to apply it."

    def teach_framework_to_peer(self, key: str, peer: "Agent") -> str:
        if key not in self.knowledge_base:
            return f"[{self.agent_id}] {self.name} has no '{key}' to teach."
        peer.knowledge_base[key] = self.knowledge_base[key]
        peer.knowledge_score = round(peer.knowledge_score + 0.05, 2)
        return f"[{self.agent_id}] {self.name} taught '{key}' to [{peer.agent_id}] {peer.name}."

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

    def _team_lead(self) -> Agent:
        for agent in self.agents:
            if agent.is_team_lead:
                return agent
        raise ValueError("No team lead configured.")

    def _find_by_name(self, name: str) -> Agent:
        for agent in self.agents:
            if agent.name == name:
                return agent
        raise ValueError(f"Agent '{name}' not found")

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
                f"[{assignee.agent_id}] {assignee.name} reports IMPORTANT '{task.title}' to team lead [{lead.agent_id}] {lead.name}."
            )

        logs.append(f"[{lead.agent_id}] {lead.name} reviews/filters the report and escalates to {self.user_name}.")

        if task.requires_approval:
            logs.append(
                f"[APPROVAL FLOW] agent -> team lead({lead.name}) -> {self.user_name} required for '{task.title}'."
            )

        return logs

    def run_team_greeting(self) -> List[str]:
        return [agent.greeting() for agent in self.agents]

    def teach_sota_engine_to_boun_and_rimo(self) -> List[str]:
        logs: List[str] = []
        for name in ["보운", "리모"]:
            agent = self._find_by_name(name)
            logs.append(agent.learn_framework("sota_expectation_engine_v3_3", SOTA_EXPECTATION_ENGINE_V3_3))
        return logs

    def recall_sota_engine(self, by_agent_name: str) -> str:
        agent = self._find_by_name(by_agent_name)
        return agent.recall_framework("sota_expectation_engine_v3_3")

    def apply_mirofish_to_team(self) -> List[str]:
        logs: List[str] = []
        lead = self._team_lead()
        for agent in self.agents:
            logs.append(agent.apply_mirofish_playbook())
            if agent.agent_id != lead.agent_id:
                logs.append(f"[{agent.agent_id}] {agent.name} routes swarm signal to lead [{lead.agent_id}] {lead.name}.")
        logs.append(f"[{lead.agent_id}] {lead.name} consolidates swarm signals and reports to {self.user_name}.")
        return logs

    def run_mirofish_schooling_cycle(self) -> List[str]:
        logs: List[str] = []
        lead = self._team_lead()
        for agent in self.agents:
            if agent.agent_id == lead.agent_id:
                continue
            agent.signal_confidence = round(min(1.0, agent.signal_confidence + 0.05), 2)
            logs.append(f"[{agent.agent_id}] {agent.name} syncs with lead {lead.name} (confidence={agent.signal_confidence}).")
        logs.append(f"[{lead.agent_id}] {lead.name} finalizes coordinated action for {self.user_name}.")
        return logs

    def spread_sota_engine_from_leads(self) -> List[str]:
        logs: List[str] = []
        boun = self._find_by_name("보운")
        rimo = self._find_by_name("리모")

        for agent in self.agents:
            if agent.name in {"보운", "리모"}:
                continue
            logs.append(boun.teach_framework_to_peer("sota_expectation_engine_v3_3", agent))
            logs.append(rimo.teach_framework_to_peer("sota_expectation_engine_v3_3", agent))
        return logs

    def run_peer_dialogue_cycle(self) -> List[str]:
        logs: List[str] = []
        for idx, speaker in enumerate(self.agents):
            listener = self.agents[(idx + 1) % len(self.agents)]
            logs.append(speaker.share_insight(listener))
        return logs

    def run_market_intel_cycle(self) -> List[str]:
        logs: List[str] = []
        lead = self._team_lead()

        for agent in self.agents:
            logs.append(agent.update_from_best_sources())
            if agent.name == "리모":
                logs.append(
                    f"[{agent.agent_id}] 리모 submits curated memecoin/crypto opportunities to team lead [{lead.agent_id}] {lead.name}."
                )
                logs.append(f"[{lead.agent_id}] {lead.name} filters Rimo's intel and reports key points to {self.user_name}.")
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
            expertise=["investment", "portfolio", "risk", "valuation-framework"],
            swarm_role="lead",
            is_team_lead=True,
        ),
        Agent(
            agent_id="agent_02",
            name="리모",
            role="Crypto & Memecoin Specialist",
            personality="fast-scout",
            creativity_style="trend hunting",
            growth_goal="track real-time crypto/memecoin alpha",
            expertise=["coin", "memecoin", "onchain", "expectation-valuation"],
            swarm_role="alpha-scout",
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
            swarm_role="macro-scout",
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
            swarm_role="risk-scout",
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
            swarm_role="execution-scout",
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
            swarm_role="synthesis-scout",
            reports_to="agent_01",
        ),
    ]
