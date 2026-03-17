from src.office_simulation import OfficeSimulation, build_default_agents


def demo() -> None:
    sim = OfficeSimulation(agents=build_default_agents(), user_name="YOU")

    print("=== STANDING GREETING ===")
    for line in sim.run_team_greeting():
        print(line)

    print("\n=== UX CRITIC LOOP (불만 <-> 조시) ===")
    for line in sim.run_ux_improvement_cycle(rounds=5):
        print(line)


if __name__ == "__main__":
    demo()
