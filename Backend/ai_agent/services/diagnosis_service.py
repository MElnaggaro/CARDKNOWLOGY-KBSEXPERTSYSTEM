from ..integration.kbs_bridge import KBSBridge

class DiagnosisService:
    """Business logic for orchestrating the diagnosis process."""
    
    def __init__(self):
        self.bridge = KBSBridge()

    def perform_diagnosis(self, patient_data: dict) -> dict:
        """Runs diagnosis and processes the result for the agent."""
        raw_result = self.bridge.call_engine(patient_data)
        
        # Add business logic processing here (e.g. tracking progress)
        return raw_result
