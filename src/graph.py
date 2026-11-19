import os
import sys
from pathlib import Path

# Ensure project root is available on sys.path
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from dotenv import load_dotenv
load_dotenv()

from langgraph.graph import StateGraph

try:
    from .state import EmailsState
    from .nodes import check_email, wait_next_run, new_emails_condition
    from .crew.crew import EmailFilterCrew
except (ImportError, ValueError):
    from src.state import EmailsState
    from src.nodes import check_email, wait_next_run, new_emails_condition
    from src.crew.crew import EmailFilterCrew

def create_workflow():
    workflow = StateGraph(EmailsState)
    crew = EmailFilterCrew()

    workflow.add_node("check_new_emails", check_email)
    workflow.add_node("wait_next_run", wait_next_run)
    workflow.add_node("draft_responses", crew.kickoff)

    workflow.set_entry_point("check_new_emails")
    workflow.add_conditional_edges(
        "check_new_emails",
        new_emails_condition,
        {
            "continue": "draft_responses",
            "end": "wait_next_run",
        },
    )
    workflow.add_edge("draft_responses", "wait_next_run")
    workflow.add_edge("wait_next_run", "check_new_emails")

    return workflow.compile()

class WorkFlow:
    """Convenience class preserving backwards compatibility."""
    def __init__(self):
        self.app = create_workflow()
