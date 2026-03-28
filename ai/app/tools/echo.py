# ai/app/tools/echo.py

def echo_message(word: str) -> str:
    """
    A simple tool that returns the provided word back to the orchestrator.
    Used to verify the hybrid (Tools + Pydantic) routing behavior.
    """
    return f"Echo from tool: {word}"
