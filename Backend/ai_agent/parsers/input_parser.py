class InputParser:
    """Parses raw user input into a structured format for the agent."""
    
    @staticmethod
    def parse_user_message(message: str) -> dict:
        """
        Extracts potential symptoms and intent from user message.
        (Basic implementation - can be enhanced with NLP)
        """
        return {
            "raw_text": message,
            "intent": "diagnosis_request",  # Default intent
            "extracted_data": {}
        }
