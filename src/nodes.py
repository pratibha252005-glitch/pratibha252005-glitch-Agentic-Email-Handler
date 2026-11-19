import os
import sys
import time
from pathlib import Path
from typing import Any, Dict

_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from langchain_community.tools.gmail.search import GmailSearch

try:
    from .crew.tools import get_gmail_toolkit
except (ImportError, ValueError):
    from src.crew.tools import get_gmail_toolkit

def check_email(state: Dict[str, Any]) -> Dict[str, Any]:
    """Poll Gmail for new emails within the past day and filter unseen threads."""
    print("# Checking for new emails")
    gmail = get_gmail_toolkit()
    if not gmail:
        print("## Error: Gmail credentials not configured. Please place credentials.json in the project root.")
        return {
            **state,
            "emails": [],
            "checked_emails_ids": state.get("checked_emails_ids") or [],
        }

    search = GmailSearch(api_resource=gmail.api_resource)
    try:
        raw_emails = search.run("after:newer_than:1d")
    except Exception as e:
        print(f"## Error querying Gmail: {e}")
        raw_emails = []

    if not isinstance(raw_emails, list):
        print("## No email list returned or error querying Gmail")
        raw_emails = []

    checked_ids = set(state.get("checked_emails_ids") or [])
    my_email = os.getenv("MY_EMAIL", "").strip().lower()

    seen_threads = set()
    new_emails = []

    for email in raw_emails:
        email_id = email.get("id")
        thread_id = email.get("threadId")
        sender = email.get("sender", "")

        if not email_id or email_id in checked_ids:
            continue
        if thread_id in seen_threads:
            continue
        if my_email and my_email in sender.lower():
            continue

        seen_threads.add(thread_id)
        new_emails.append({
            "id": email_id,
            "threadId": thread_id,
            "snippet": email.get("snippet", ""),
            "sender": sender,
        })
        checked_ids.add(email_id)

    return {
        **state,
        "emails": new_emails,
        "checked_emails_ids": list(checked_ids),
    }

def wait_next_run(state: Dict[str, Any]) -> Dict[str, Any]:
    """Wait before the next poll cycle. Configurable via EMAIL_POLL_INTERVAL."""
    delay = int(os.getenv("EMAIL_POLL_INTERVAL", "180"))
    print(f"## Waiting for {delay} seconds before next check")
    time.sleep(delay)
    return state

def new_emails_condition(state: Dict[str, Any]) -> str:
    """Conditional routing based on whether new emails were found."""
    if state.get("emails"):
        print(f"## Found {len(state['emails'])} new emails to process")
        return "continue"
    print("## No new emails found")
    return "end"

class Nodes:
    """Convenience class preserving backwards compatibility."""
    def check_email(self, state):
        return check_email(state)

    def wait_next_run(self, state):
        return wait_next_run(state)

    def new_emails(self, state):
        return new_emails_condition(state)
