import os
from typing import Optional

try:
    from crewai.tools import tool
except ImportError:
    from langchain_core.tools import tool
from langchain_community.agent_toolkits import GmailToolkit
from langchain_community.tools.gmail.create_draft import GmailCreateDraft

_gmail_toolkit: Optional[GmailToolkit] = None

def get_gmail_toolkit() -> Optional[GmailToolkit]:
    """Lazily initialize and cache the GmailToolkit instance."""
    global _gmail_toolkit
    if _gmail_toolkit is None:
        try:
            _gmail_toolkit = GmailToolkit()
        except Exception as e:
            print(f"[GmailToolkit] Notice: Could not initialize Gmail API ({e}). Ensure credentials.json exists.")
            return None
    return _gmail_toolkit

@tool("create_draft")
def create_draft(data: str) -> str:
    """Useful to create an email draft.
    The input must be formatted as pipe-separated text: 'recipient|subject|message'.
    Example: lorem@ipsum.com|Project Update|Here is the latest progress report.
    """
    parts = [part.strip() for part in data.split("|", 2)]
    if len(parts) < 3:
        return "Error: Input must contain recipient, subject, and message separated by '|'."

    recipient, subject, message = parts
    toolkit = get_gmail_toolkit()
    if not toolkit:
        return "Error: Gmail credentials not configured. Please place credentials.json in project root."

    draft = GmailCreateDraft(api_resource=toolkit.api_resource)
    result = draft.run({"to": [recipient], "subject": subject, "message": message})
    return f"Draft created: {result}"

class CreateDraftTool:
    """Backwards compatibility alias for CreateDraftTool.create_draft."""
    create_draft = create_draft

