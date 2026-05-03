from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class AgentResponse:
    """Schema for a response from the AI Agent."""
    agent_id: str
    message: str
    action_taken: str
    data: Dict = field(default_factory=dict)
    urgency_alert: Optional[str] = None
