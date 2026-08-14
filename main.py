import uuid
from langgraph.checkpoint.sqlite import SqliteSaver
from services.db import ChatDatabase
from agents.orchestrator import run_orchestrator



def main():
    with SqliteSaver.from_conn_string("chat_history.db") as checkpointer:
        print("NAMS: Вітаю! Чим я можу вам допомогти?")
        db = ChatDatabase()
        db.create_table()
        session_id = str(uuid.uuid4())

        while True:
            user_input = input("\nYou: ")
            db.save_message(session_id, "user", user_input)


            response = run_orchestrator(user_input, session_id, checkpointer)
            if response:
                db.save_message(session_id, "assistant", response)
            else:
                print("Не вдалося отримати відповідь, повідомлення не збережено.")

if __name__ == "__main__":
    main()