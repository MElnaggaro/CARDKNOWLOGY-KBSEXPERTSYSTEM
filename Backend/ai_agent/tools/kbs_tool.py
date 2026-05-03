import sys
import os

# Add the Backend directory to sys.path if needed
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

try:
    from kbs.engine.runner import run_diagnosis
except ImportError:
    # If running from outside the Backend directory
    try:
        from Backend.kbs.engine.runner import run_diagnosis
    except ImportError:
        # Final fallback for cases where neither works directly
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
        from kbs.engine.runner import run_diagnosis

class KBSTool:
    """Tool for interacting with the Expert System Engine."""
    
    @staticmethod
    def execute(data: dict) -> dict:
        """
        Runs the KBS diagnosis engine.
        Expects categorized data: {"symptoms": {...}, "vitals": {...}, "background": {...}}
        """
        try:
            result = run_diagnosis(data)
            return result
        except Exception as e:
            return {"error": f"KBS Engine error: {str(e)}"}
