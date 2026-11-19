from crewai import Agent, Task

def create_filter_task(agent: Agent, emails: str) -> Task:
    return Task(
        description=(
            "Analyze the batch of emails below and filter out non-essential messages "
            "(newsletters, promotional content, automated notifications).\n\n"
            f"EMAILS:\n{emails}\n\n"
            "Return a bulleted list of relevant thread IDs and senders requiring human review."
        ),
        expected_output="Bulleted list with thread_id and sender for each relevant email.",
        agent=agent,
    )

def create_action_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Pull and review the complete email threads using the identified Thread IDs.\n"
            "For each thread, identify:\n"
            "- Thread ID\n"
            "- Key discussion points and user questions\n"
            "- Sender email address\n"
            "- Urgency and expected response style"
        ),
        expected_output="Structured summary of each action-required email thread.",
        agent=agent,
    )

def create_draft_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Draft targeted responses for each action-required email thread.\n"
            "- Research necessary background information using Tavily if needed.\n"
            "- Use the 'Create Draft' tool to save each draft in Gmail.\n"
            "- Format tool input as: recipient|subject|body."
        ),
        expected_output="Confirmation of all email drafts created in Gmail.",
        agent=agent,
    )

class EmailFilterTasks:
    """Convenience class preserving backwards compatibility."""
    def filter_emails_task(self, agent, emails):
        return create_filter_task(agent, emails)

    def action_required_emails_task(self, agent):
        return create_action_task(agent)

    def draft_responses_task(self, agent):
        return create_draft_task(agent)
