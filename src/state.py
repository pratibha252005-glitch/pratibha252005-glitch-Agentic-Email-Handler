from typing import Any, Dict, List, Optional, TypedDict

class EmailsState(TypedDict, total=False):
    checked_emails_ids: List[str]
    emails: List[Dict[str, Any]]
    action_required_emails: Optional[Any]
