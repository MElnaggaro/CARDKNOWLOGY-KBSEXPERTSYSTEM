class MemoryTool:
    """Tool for updating agent's internal memory/facts."""
    
    def __init__(self, session_memory):
        self.session_memory = session_memory

    def execute(self, category: str, facts: dict) -> dict:
        """Updates session memory with new facts."""
        self.session_memory.update_facts(category, facts)
        return {"status": "success", "updated_category": category}
