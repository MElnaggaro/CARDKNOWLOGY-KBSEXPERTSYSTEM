import json
import os

class Storage:
    """Handles JSON-based persistence for agent memory."""
    
    @staticmethod
    def save(data: dict, filepath: str):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load(filepath: str) -> dict:
        if not os.path.exists(filepath):
            return {}
        with open(filepath, 'r') as f:
            return json.load(f)
