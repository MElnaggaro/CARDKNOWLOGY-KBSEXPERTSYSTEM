import json
import os
from pathlib import Path

class SessionMemory:
    """Manages the state of the current conversation session and persists patient data."""
    
    def __init__(self, storage_file="patient_history.json"):
        self.history = []
        self.current_context = {}
        self.collected_facts = {
            "symptoms": {},
            "vitals": {},
            "background": {}
        }
        self.storage_path = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", storage_file)))
        self._load_from_storage()

    def _load_from_storage(self):
        """Loads persistent data from file if it exists."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, 'r') as f:
                    stored_data = json.load(f)
                    # We only load the facts into the current session if we want to 'remember' them
                    # For now, let's just keep them in a history list and allow the agent to query them
                    self.persistent_history = stored_data.get("history", [])
                    # Also pre-fill collected facts with the latest known state to 'keep' the data
                    latest_state = stored_data.get("latest_facts", {})
                    for category in self.collected_facts:
                        if category in latest_state:
                            self.collected_facts[category].update(latest_state[category])
            except Exception as e:
                print(f"Error loading memory: {e}")
                self.persistent_history = []
        else:
            self.persistent_history = []

    def _save_to_storage(self):
        """Saves current state to persistent storage."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        data_to_save = {
            "latest_facts": self.collected_facts,
            "history": self.persistent_history + [{"timestamp": os.path.getmtime(self.storage_path) if self.storage_path.exists() else None, "facts": self.collected_facts}]
        }
        # Keep history reasonable
        if len(data_to_save["history"]) > 50:
            data_to_save["history"] = data_to_save["history"][-50:]
            
        with open(self.storage_path, 'w') as f:
            json.dump(data_to_save, f, indent=4)

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def update_facts(self, category: str, facts: dict):
        if category in self.collected_facts:
            self.collected_facts[category].update(facts)
            self._save_to_storage() # Persist every time facts are updated

    def get_all_facts(self) -> dict:
        return self.collected_facts

    def clear(self):
        self.history = []
        self.current_context = {}
        # We don't clear persistent memory unless explicitly told to
        # But we clear the 'session' facts if needed. 
        # Actually, the user wants to 'keep' data, so maybe we don't clear it.
        # self.collected_facts = {"symptoms": {}, "vitals": {}, "background": {}}
