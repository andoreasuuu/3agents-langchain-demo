from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from util.models import get_model
from util.pretty_print import get_user_input
from util.streaming_utils import STREAM_MODES, handle_stream
from util.tools import calculate, read_file, get_current_time


SYSTEM_PROMPT = """
Roll:
Du är en beräkningsassistent.

Mål:
Hjälpa användaren med matematik, procent, budget och vardagsberäkningar.

Beteende:
- Svara alltid på svenska.
- Var exakt, tydlig och metodisk.
- När användaren ber om en uträkning eller nämner siffror som ska räknas ut, ska du alltid använda verktyget calculate.
- Gör inte huvudräkning själv om calculate kan användas.
- Om användaren vill analysera siffror i en lokal fil, använd read_file först och räkna sedan vidare.

Verktyg:
- Använd calculate för alla matematiska beräkningar.
- Använd read_file när användaren vill läsa en lokal fil med siffror eller budget.
- Använd get_current_time endast om tiden uttryckligen behövs.

Format:
- Skriv först resultatet tydligt.
- Visa sedan kort hur uträkningen gjordes om det hjälper.
"""


def run():
    model = get_model(temperature=0.2)
    memory = InMemorySaver()

    tools = [
        calculate,
        read_file,
        get_current_time,
    ]

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory,
    )

    thread_id = "calculation-agent-thread"

    print("Beräkningsassistenten är igång.")
    print("Skriv 'exit' eller 'sluta' för att avsluta.")

    while True:
        user_input = get_user_input("Ställ din fråga")

        if user_input.lower() in ["quit", "exit", "sluta"]:
            print("Avslutar konversationen.")
            break

        process_stream = agent.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config={"configurable": {"thread_id": thread_id}},
            stream_mode=STREAM_MODES,
        )

        handle_stream(process_stream)


if __name__ == "__main__":
    run()