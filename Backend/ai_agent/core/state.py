from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class AgentState:
    """Represents the current state of the AI Agent."""
    is_running: bool = True
    last_action: str = ""
    last_observation: Dict[str, Any] = field(default_factory=dict)
    waiting_for_user: bool = False
    error_count: int = 0
