import sys
from pathlib import Path
from typing import Any, Dict, List

_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from crewai import Crew

try:
    from .agents import create_action_agent, create_filter_agent, create_writer_agent
    from .tasks import create_action_task, create_draft_task, create_filter_task
except (ImportError, ValueError):
    from src.crew.agents import create_action_agent, create_filter_agent, create_writer_agent
    from src.crew.tasks import create_action_task, create_draft_task, create_filter_task

def format_emails(emails: List[Dict[str, Any]]) -> str:
    """Format raw email dictionaries into structured text for agent consumption."""
    if not emails:
        return "No emails to process."
    return "\n\n".join(
        f"ID: {e.get('id')}\n"
        f"Thread ID: {e.get('threadId')}\n"
        f"From: {e.get('sender')}\n"
        f"Snippet: {e.get('snippet')}\n"
        "--------"
        for e in emails
    )

class EmailFilterCrew:
    def __init__(self):
        self.filter_agent = create_filter_agent()
        self.action_agent = create_action_agent()
        self.writer_agent = create_writer_agent()

    def kickoff(self, state: Dict[str, Any]) -> Dict[str, Any]:
        emails = state.get("emails", [])
        if not emails:
            return {**state, "action_required_emails": None}

        formatted = format_emails(emails)
        crew = Crew(
            agents=[self.filter_agent, self.action_agent, self.writer_agent],
            tasks=[
                create_filter_task(self.filter_agent, formatted),
                create_action_task(self.action_agent),
                create_draft_task(self.writer_agent),
            ],
            verbose=True,
        )
        result = crew.kickoff()
        return {**state, "action_required_emails": result}
