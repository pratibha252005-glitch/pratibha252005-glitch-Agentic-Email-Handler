import sys
from pathlib import Path

# Ensure package root is available on sys.path
_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from langchain_community.tools.gmail.get_thread import GmailGetThread
from langchain_community.tools.tavily_search import TavilySearchResults
from crewai import Agent

try:
    from .tools import create_draft, get_gmail_toolkit
except (ImportError, ValueError):
    from src.crew.tools import create_draft, get_gmail_toolkit

def _get_tavily_tool():
    """Safely initialize Tavily search tool without crashing if API key is not yet set."""
    try:
        return TavilySearchResults()
    except Exception as e:
        print(f"[Tavily] Notice: Tavily search disabled ({e}). Set TAVILY_API_KEY in .env to enable.")
        return None

def create_filter_agent() -> Agent:
    return Agent(
        role="Senior Email Analyst",
        goal="Filter out non-essential emails (newsletters, spam, automated alerts).",
        backstory=(
            "Expert in email triage with an eye for distinguishing critical correspondence "
            "from newsletters, promotional blasts, and automated notifications."
        ),
        verbose=True,
        allow_delegation=False,
    )

def create_action_agent() -> Agent:
    gmail = get_gmail_toolkit()
    tools = []
    tavily = _get_tavily_tool()
    if tavily:
        tools.append(tavily)
    if gmail:
        tools.append(GmailGetThread(api_resource=gmail.api_resource))
    return Agent(
        role="Email Action Specialist",
        goal="Identify emails requiring immediate action and extract key context.",
        backstory=(
            "Specialist in analyzing email threads to determine priority, "
            "urgency, and required next steps from stakeholders."
        ),
        tools=tools,
        verbose=True,
        allow_delegation=False,
    )

def create_writer_agent() -> Agent:
    gmail = get_gmail_toolkit()
    tools = [create_draft]
    tavily = _get_tavily_tool()
    if tavily:
        tools.append(tavily)
    if gmail:
        tools.append(GmailGetThread(api_resource=gmail.api_resource))
    return Agent(
        role="Email Response Writer",
        goal="Draft clear, context-aware email responses for action-required items.",
        backstory=(
            "Skilled communicator capable of adopting the user's voice and crafting "
            "tailored, professional responses to resolve thread inquiries."
        ),
        tools=tools,
        verbose=True,
        allow_delegation=False,
    )

class EmailFilterAgents:
    """Convenience class preserving backwards compatibility."""
    def __init__(self):
        pass

    def email_filter_agent(self):
        return create_filter_agent()

    def email_action_agent(self):
        return create_action_agent()

    def email_response_writer(self):
        return create_writer_agent()
