import sys
import os

# Add the Backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

try:
    from kbs.engine.runner import run_diagnosis
except ImportError:
    try:
        from Backend.kbs.engine.runner import run_diagnosis
    except ImportError:
        # Absolute path fix for nested execution
        import sys
        import os
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
        from kbs.engine.runner import run_diagnosis

class KBSBridge:
    """
    Acts as a bridge between the AI Agent and the Expert System Engine.
    Handles data translation and high-level KBS orchestration.
    """
    
    def __init__(self):
        self.engine = run_diagnosis

    def call_engine(self, facts: dict) -> dict:
        """
        Translates agent facts into engine-compatible format and calls the runner.
        """
        # Ensure data is categorized correctly
        categorized_data = {
            "symptoms": facts.get("symptoms", {}),
            "vitals": facts.get("vitals", {}),
            "background": facts.get("background", {})
        }
        
        try:
            return self.engine(categorized_data)
        except Exception as e:
            return {"error": str(e), "status": "failed"}
