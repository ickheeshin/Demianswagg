from src.office_simulation import OfficeSimulation, Task, build_default_agents


def demo() -> None:
    sim = OfficeSimulation(agents=build_default_agents(), user_name="YOU")

    tasks = [
        Task(title="BTC 변동성 보고서", category="coin", priority=3),
        Task(title="밈코인 급등 후보 탐지", category="memecoin", priority=5, important=True),
        Task(title="고위험 포지션 승인 요청", category="investment", priority=4, important=True, requires_approval=True),
    ]

    print("=== TEAM GREETING ===")
    for line in sim.run_team_greeting():
        print(line)

    print("\n=== SOTA ENGINE TRAINING (BOUN + RIMO) ===")
    for line in sim.teach_sota_engine_to_boun_and_rimo():
        print(line)

    print("\n=== SOTA ENGINE SPREAD ===")
    for line in sim.spread_sota_engine_from_leads():
        print(line)

    print("\n=== SOTA ENGINE RECALL CHECK ===")
    print(sim.recall_sota_engine("보운"))
    print(sim.recall_sota_engine("리모"))
    print(sim.recall_sota_engine("TBD-3"))

    print("\n=== WORK MODE ===")
    for line in sim.assign_tasks(tasks):
        print(line)

    print("\n=== PEER DIALOGUE / KNOWLEDGE SHARE ===")
    for line in sim.run_peer_dialogue_cycle():
        print(line)

    print("\n=== MARKET INTEL UPDATE ===")
    for line in sim.run_market_intel_cycle():
        print(line)

    print("\n=== GROWTH CYCLE ===")
    for line in sim.run_growth_cycle():
        print(line)

    print("\n=== IDLE MODE ===")
    for line in sim.assign_tasks([]):
        print(line)


if __name__ == "__main__":
    demo()
