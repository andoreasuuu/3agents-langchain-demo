import math
from pathlib import Path
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup
from langchain.tools import tool


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression and return the result."""
    allowed_names = {
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sqrt": math.sqrt,
        "pow": pow,
        "pi": math.pi,
        "e": math.e,
    }

    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"{expression} = {result}"
    except Exception as e:
        return f"Error evaluating '{expression}': {e}"


@tool
def get_current_time() -> str:
    """Get the current date and time in UTC."""
    now = datetime.now(timezone.utc)
    return f"Current UTC time: {now.strftime('%Y-%m-%d %H:%M:%S UTC')}"


@tool
def read_file(file_path: str) -> str:
    """Read a local text-based file and return its contents."""
    try:
        path = Path(file_path)

        if not path.exists():
            return f"Filen finns inte: {file_path}"

        if not path.is_file():
            return f"Sökvägen är inte en fil: {file_path}"

        if path.suffix.lower() not in [".txt", ".md", ".py", ".json", ".csv"]:
            return "Den här versionen stöder bara vanliga textfiler."

        content = path.read_text(encoding="utf-8")

        if len(content) > 5000:
            content = content[:5000] + "\n\n[Innehållet är trunkerat]"

        return f"Innehåll i {file_path}:\n\n{content}"

    except Exception as e:
        return f"Kunde inte läsa filen '{file_path}': {e}"


@tool
def read_webpage(url: str) -> str:
    """Fetch a webpage and return the cleaned main text content."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "noscript", "header", "footer"]):
            tag.decompose()

        text = " ".join(soup.stripped_strings)

        if not text:
            return f"Kunde inte läsa någon text från sidan: {url}"

        if len(text) > 5000:
            text = text[:5000] + "\n\n[Webbsidans innehåll är trunkerat]"

        return f"Innehåll från {url}:\n\n{text}"

    except Exception as e:
        return f"Kunde inte läsa webbsidan '{url}': {e}"