class Planner:
    """Decides the next course of action based on current state and LLM feedback."""
    
    def __init__(self, llm_client, prompt_builder):
        self.llm_client = llm_client
        self.prompt_builder = prompt_builder

    def plan(self, user_input: str, history: list, facts: dict) -> str:
        """Asks the LLM to decide the next action."""
        system_prompt = self.prompt_builder.build_system_prompt()
        user_prompt = self.prompt_builder.build_user_prompt(user_input, history, facts)
        
        return self.llm_client.complete(user_prompt, system_prompt)
