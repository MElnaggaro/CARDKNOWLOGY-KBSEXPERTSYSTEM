class PromptBuilder:
    """Constructs system and user prompts for the agent."""
    
    @staticmethod
    def build_system_prompt() -> str:
        return """
        You are CardKnowlogy Agent, a medical AI assistant specializing in cardiac health.
        Your goal is to help diagnose potential cardiac conditions by interacting with a Knowledge-Based System (KBS).
        
        Rules:
        1. Always ask clarifying questions if symptoms are vague.
        2. Use tools to interact with the KBS engine.
        3. Provide urgency alerts if vital signs are critical.
        4. Return your response in JSON format specifying an 'action' and 'parameters'.
        """

    @staticmethod
    def build_user_prompt(user_input: str, history: list, facts: dict) -> str:
        return f"""
        User Input: {user_input}
        
        Current Facts: {facts}
        
        Recent History: {history[-5:]}
        
        Decide the next action.
        """
