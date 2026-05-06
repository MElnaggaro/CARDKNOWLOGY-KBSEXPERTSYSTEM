import json
import os
from pathlib import Path
from datetime import datetime

def format_output_file(data, filepath):
    """
    Writes the diagnostic result data to a JSON file.
    Adds a timestamp to the output.
    """
    path = Path(filepath)
    
    # Ensure directory exists
    path.parent.mkdir(parents=True, exist_ok=True)
    
    output_payload = {
        "timestamp": datetime.now().isoformat(),
        "status": "success" if data else "error",
        "result": data
    }
    
    try:
        with open(path, 'w') as f:
            json.dump(output_payload, f, indent=4)
        print(f"Output successfully written to {filepath}")
    except IOError as e:
        print(f"Error writing to output file: {e}")
