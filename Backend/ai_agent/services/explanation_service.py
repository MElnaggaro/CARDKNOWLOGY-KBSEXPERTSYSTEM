class ExplanationService:
    """Generates human-friendly explanations for diagnosis results."""
    
    @staticmethod
    def simplify_explanation(raw_explanation: dict) -> str:
        """Converts internal engine explanation into a friendly string."""
        if not raw_explanation:
            return "No specific explanation available."
            
        rules_triggered = raw_explanation.get("rules_triggered", [])
        if not rules_triggered:
            return "The system reached this conclusion based on general cardiac patterns."
            
        return f"Based on your symptoms, the system identified matches with {len(rules_triggered)} diagnostic rules."
