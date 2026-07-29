from agents.orchestrator import run_orchestrator

if __name__ == "__main__":
    while True:
        response = run_orchestrator(input(f"\nYou: "))
        print(response)