from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class AgentRequest:
    """Schema for a request to the AI Agent."""
    user_id: str
    message: str
    context: Dict = field(default_factory=dict)
    metadata: Optional[Dict] = None
