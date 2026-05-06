from .kbs_tool import KBSTool
from .alert_tool import AlertTool
from .memory_tool import MemoryTool

class ToolExecutor:
    """Dispatches tool calls from the agent."""
    
    def __init__(self, session_memory):
        self.session_memory = session_memory
        self.kbs_tool = KBSTool()
        self.alert_tool = AlertTool()
        self.memory_tool = MemoryTool(session_memory)

    def execute(self, action: str, parameters: dict) -> dict:
        """Executes the specified action with parameters."""
        if action == "call_kbs":
            # Merge current facts from memory with new parameters
            current_facts = self.session_memory.get_all_facts()
            
            # Shallow merge categories
            merged_data = {
                "symptoms": {**current_facts.get("symptoms", {}), **parameters.get("symptoms", {})},
                "vitals": {**current_facts.get("vitals", {}), **parameters.get("vitals", {})},
                "background": {**current_facts.get("background", {}), **parameters.get("background", {})}
            }
            
            # Perform assessment
            result = self.kbs_tool.execute(merged_data)
            
            # After assessment, update memory with the symptoms/vitals used
            for cat in ["symptoms", "vitals", "background"]:
                if cat in parameters:
                    self.session_memory.update_facts(cat, parameters[cat])
            
            return result
        elif action == "alert":
            return self.alert_tool.execute(**parameters)
        elif action == "update_memory":
            category = parameters.get("category")
            facts = parameters.get("facts", {})
            if category:
                return self.memory_tool.execute(category, facts)
            return {"error": "Missing category in update_memory"}
        elif action == "speak":
            return {"message": parameters.get("message", "")}
        else:
            return {"error": f"Unknown action: {action}"}
