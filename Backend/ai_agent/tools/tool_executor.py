from .kbs_tool import KBSTool
from .alert_tool import AlertTool
from .memory_tool import MemoryTool

class ToolExecutor:
    """Dispatches tool calls from the agent."""
    
    def __init__(self, session_memory):
        self.kbs_tool = KBSTool()
        self.alert_tool = AlertTool()
        self.memory_tool = MemoryTool(session_memory)

    def execute(self, action: str, parameters: dict) -> dict:
        """Executes the specified action with parameters."""
        if action == "call_kbs":
            return self.kbs_tool.execute(parameters)
        elif action == "alert":
            return self.alert_tool.execute(**parameters)
        elif action == "update_memory":
            return self.memory_tool.execute(**parameters)
        elif action == "speak":
            return {"message": parameters.get("message", "")}
        else:
            return {"error": f"Unknown action: {action}"}
