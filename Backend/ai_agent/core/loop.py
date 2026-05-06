class AgentLoop:
    """The main execution loop of the agent (Observe -> Plan -> Execute)."""
    
    def __init__(self, agent):
        self.agent = agent

    def run_step(self, user_input: str):
        """Executes a single step of the agent loop."""
        # 1. Observe (Parse user input)
        observation = self.agent.input_parser.parse_user_message(user_input)
        
        # 2. Plan (Ask LLM or Planner for action)
        raw_plan = self.agent.planner.plan(
            observation["raw_text"], 
            self.agent.memory.history, 
            self.agent.memory.get_all_facts()
        )
        
        # 3. Execute (Run tool)
        action_data = self.agent.output_parser.parse_llm_action(raw_plan)
        result = self.agent.tool_executor.execute(
            action_data.get("action"), 
            action_data.get("parameters", {})
        )
        
        # 4. Update Memory
        self.agent.memory.add_message("user", user_input)
        if "message" in result:
            self.agent.memory.add_message("agent", result["message"])
            
        # Add memory snapshot for the UI/Report
        result["memory_snapshot"] = self.agent.memory.get_all_facts()
            
        return result
