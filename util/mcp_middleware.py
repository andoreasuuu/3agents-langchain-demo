from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage


@wrap_tool_call
async def clean_mcp_tool_output(request, handler):
    """
    Bearbetar output från MCP-tools innan agenten får resultatet.
    Async-version eftersom agenten körs med astream().
    """
    try:
        result = await handler(request)
    except Exception as e:
        tool_call_id = None

        if hasattr(request, "tool_call") and request.tool_call:
            tool_call_id = request.tool_call.get("id")

        return ToolMessage(
            content=f"Tool error: {e}",
            tool_call_id=tool_call_id or "unknown",
        )

    if isinstance(result, ToolMessage):
        content = str(result.content)

        replacements = {
            '"status": "success"': "Status: OK",
            '"status": "error"': "Status: FEL",
            "estimated_hours": "beräknade_timmar",
            "priority_score": "prioritetspoäng",
            "assignments": "uppgifter",
            "prioritized": "prioriterade_uppgifter",
            "summary": "sammanfattning",
        }

        for old, new in replacements.items():
            content = content.replace(old, new)

        return ToolMessage(
            content=f"Bearbetat verktygsresultat:\n{content}",
            tool_call_id=result.tool_call_id,
        )

    return result