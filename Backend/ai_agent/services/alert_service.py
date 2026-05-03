class AlertService:
    """Service for managing medical alerts and urgency levels."""
    
    @staticmethod
    def evaluate_urgency(vitals: dict, diagnosis_result: dict) -> dict:
        """Determines if immediate medical attention is required."""
        urgency = diagnosis_result.get("urgency", "NORMAL")
        confidence = diagnosis_result.get("confidence", 0)
        
        is_critical = urgency == "CRITICAL"
        
        return {
            "is_critical": is_critical,
            "urgency": urgency,
            "alert_message": "EMERGENCY: Please seek immediate medical help!" if is_critical else "Monitor symptoms closely."
        }
