from src.office_simulation import OfficeSimulation, build_default_agents


def demo() -> None:
    sim = OfficeSimulation(agents=build_default_agents(), user_name="YOU")

    print("=== STANDING GREETING ===")
    for line in sim.run_team_greeting():
        print(line)

    print("\n=== USER COMMANDED UX LOOP (불만 -> 조시) ===")
    command = "UI 전체 점검하고 미친듯이 문제 찾아서 조시가 바로 고치게 해"
    for line in sim.run_user_commanded_ux_loop(command=command, rounds=5):
        print(line)


if __name__ == "__main__":
    demo()
