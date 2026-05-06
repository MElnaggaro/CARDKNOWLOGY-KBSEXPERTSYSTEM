import json
import os
from pathlib import Path

def parse_input_file(filepath):
    """
    Reads a JSON file from the given path and returns the data.
    If the file doesn't exist or is invalid JSON, returns None.
    """
    path = Path(filepath)
    if not path.exists():
        return None
        
    try:
        with open(path, 'r') as f:
            content = f.read().strip()
            if not content:
                return None
            return json.loads(content)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error parsing input file: {e}")
        return None

def clear_input_file(filepath):
    """Clears the input file content after processing."""
    try:
        with open(filepath, 'w') as f:
            f.write("")
    except IOError as e:
        print(f"Error clearing input file: {e}")
