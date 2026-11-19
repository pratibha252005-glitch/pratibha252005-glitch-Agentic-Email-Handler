import sys
from pathlib import Path

# Ensure project root is available on sys.path
_project_root = Path(__file__).resolve().parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from src.graph import create_workflow

def main():
    print("Starting CrewAI + LangGraph Email Automation...")
    app = create_workflow()
    initial_state = {
        "checked_emails_ids": [],
        "emails": [],
        "action_required_emails": None,
    }
    try:
        app.invoke(initial_state)
    except KeyboardInterrupt:
        print("\nWorkflow stopped by user.")
        sys.exit(0)

if __name__ == "__main__":
    main()
