from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

from util.models import get_model
from util.pretty_print import get_user_input
from util.streaming_utils import STREAM_MODES, handle_stream
from util.tools import calculate, read_file, read_webpage


SYSTEM_PROMPT = """
Roll:
Du är en rese- och researchassistent.

Mål:
Hjälpa användaren att undersöka resmål, jämföra alternativ och sammanfatta information från webbsidor och lokala anteckningar.

Beteende:
- Svara alltid på svenska.
- Var praktisk, tydlig och jämförande.
- Fokusera på användbar information.
- Sammanfatta hellre tydligt än långt.

Verktyg:
- Använd read_webpage när användaren ger dig en specifik URL att läsa.
- Använd read_file när användaren vill läsa lokala anteckningar, planer eller resefiler.
- Använd calculate när användaren vill räkna på budget, kostnader eller jämförelser.
- Använd inte verktyg i onödan.

Format:
- Strukturera gärna svaret i delar som:
  1. Översikt
  2. Fördelar
  3. Nackdelar
  4. Rekommendation
"""


def run():
    model = get_model(temperature=0.4)
    memory = InMemorySaver()

    tools = [
        calculate,
        read_file,
        read_webpage,
    ]

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory,
    )

    thread_id = "travel-research-thread"

    print("Rese-/researchagenten är igång.")
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