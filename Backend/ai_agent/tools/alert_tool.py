class AlertTool:
    """Handles CF alert logic and urgency notifications."""
    
    @staticmethod
    def execute(urgency: str, confidence: float) -> dict:
        """
        Processes urgency and confidence to generate appropriate alerts.
        """
        alert_level = "info"
        if urgency == "CRITICAL" or confidence > 0.9:
            alert_level = "high"
        elif urgency == "HIGH":
            alert_level = "medium"
            
        return {
            "alert_level": alert_level,
            "message": f"Urgency level: {urgency}. Confidence: {confidence*100:.1f}%"
        }
