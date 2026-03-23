import asyncio
from pathlib import Path

from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_mcp_adapters.client import MultiServerMCPClient

from util.models import get_model
from util.pretty_print import get_user_input
from util.streaming_utils import STREAM_MODES, handle_stream_async
from util.mcp_middleware import clean_mcp_tool_output


SYSTEM_PROMPT = """
Roll:
Du är en studieassistent.

Mål:
Hjälpa användaren att prioritera skoluppgifter, uppskatta studietid
och få överblick över vad som återstår.

Beteende:
- Svara alltid på svenska.
- Var tydlig, konkret och metodisk.
- Använd bara de verktyg du faktiskt har tillgång till.
- Om användaren ber om något som kräver ett verktyg du inte har,
  säg det tydligt.
- Hitta inte på information om uppgifter som inte finns i verktygsresultaten.

Verktyg:
- Använd list_assignments för att visa uppgifter.
- Använd prioritize_assignments för att avgöra vad som bör göras först.
- Använd estimate_study_time för att uppskatta hur lång tid en uppgift kan ta.
- Använd get_assignment_summary för att ge en översikt.

Format:
- Skriv först svaret tydligt.
- Visa sedan kort varför.
"""


ALLOWED_TOOL_NAMES = {
    "list_assignments",
    "estimate_study_time",
    "prioritize_assignments",
    "get_assignment_summary",
}


def get_mcp_server_path():
    """
    Förväntad struktur:

    parent-folder/
    ├─ 3agents-langchain-demo/
    └─ study-mcp-server/
    """
    current_file = Path(__file__).resolve()
    agent_project_root = current_file.parents[2]
    mcp_server_path = agent_project_root.parent / "study-mcp-server" / "server.py"
    return str(mcp_server_path.resolve())


async def run():
    model = get_model(temperature=0.2)
    memory = InMemorySaver()

    client = MultiServerMCPClient(
        {
            "study_tools": {
                "url": "http://127.0.0.1:8000/mcp",
                "transport": "streamable_http",
            }
        }
    )

    all_tools = await client.get_tools()

    # Filtrering sker här i agent-projektet, inte i MCP-servern
    tools = [tool for tool in all_tools if tool.name in ALLOWED_TOOL_NAMES]

    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=memory,
        middleware=[clean_mcp_tool_output],
    )

    thread_id = "mcp-assignment-agent-thread"

    print("Studieagenten med MCP är igång.")
    print("Skriv 'exit' eller 'sluta' för att avsluta.")

    while True:
        user_input = get_user_input("Ställ din fråga")

        if user_input.lower() in ["quit", "exit", "sluta"]:
            print("Avslutar konversationen.")
            break

        process_stream = agent.astream(
            {"messages": [{"role": "user", "content": user_input}]},
            config={"configurable": {"thread_id": thread_id}},
            stream_mode=STREAM_MODES,
        )

        await handle_stream_async(process_stream)


if __name__ == "__main__":
    asyncio.run(run())