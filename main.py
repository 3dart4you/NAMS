import uuid
from services.db import ChatDatabase
from agents.orchestrator import run_orchestrator

session_chat = []

def main():
    print("NAMS: Вітаю! Чим я можу вам допомогти?")
    db = ChatDatabase()
    db.create_table()
    session_id = str(uuid.uuid4())

    while True:
        user_input = input("\nYou: ")
        db.save_message(session_id, "user", user_input)
        session_chat.append({"role": "user", "content": user_input})

        print("\n🤔 NAMS думає...", end="", flush=True)
        response = run_orchestrator(session_chat)
        if response:
            db.save_message(session_id, "assistant", response)
            session_chat.append({"role": "assistant", "content": response})
        else:
            print("Не вдалося отримати відповідь, повідомлення не збережено.")

if __name__ == "__main__":
    main()