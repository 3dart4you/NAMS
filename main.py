import uuid
from services.db import ChatDatabase
from agents.orchestrator import run_orchestrator


def main():
    print("NAMS: Вітаю! Чим я можу вам допомогти?")
    db = ChatDatabase()
    db.create_table()
    session_id = str(uuid.uuid4())

    while True:
        user_input = input("\nYou: ")
        db.save_message(session_id, "user", user_input)


        response = run_orchestrator(user_input, session_id)
        if response:
            db.save_message(session_id, "assistant", response)
        else:
            print("Не вдалося отримати відповідь, повідомлення не збережено.")

if __name__ == "__main__":
    main()