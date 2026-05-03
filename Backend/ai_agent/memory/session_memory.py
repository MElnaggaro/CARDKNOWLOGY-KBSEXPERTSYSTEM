class SessionMemory:
    """Manages the state of the current conversation session."""
    
    def __init__(self):
        self.history = []
        self.current_context = {}
        self.collected_facts = {
            "symptoms": {},
            "vitals": {},
            "background": {}
        }

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def update_facts(self, category: str, facts: dict):
        if category in self.collected_facts:
            self.collected_facts[category].update(facts)

    def get_all_facts(self) -> dict:
        return self.collected_facts

    def clear(self):
        self.history = []
        self.current_context = {}
        self.collected_facts = {"symptoms": {}, "vitals": {}, "background": {}}
