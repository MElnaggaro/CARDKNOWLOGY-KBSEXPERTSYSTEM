from .loop import AgentLoop
from .planner import Planner
from .state import AgentState
from ..memory.session_memory import SessionMemory
from ..llm.client import LLMClient
from ..llm.prompt_builder import PromptBuilder
from ..parsers.input_parser import InputParser
from ..parsers.output_parser import OutputParser
from ..tools.tool_executor import ToolExecutor

class CardKnowlogyAgent:
    """The main entry point for the CardKnowlogy AI Agent."""
    
    def __init__(self):
        self.state = AgentState()
        self.memory = SessionMemory()
        self.llm_client = LLMClient()
        self.prompt_builder = PromptBuilder()
        self.input_parser = InputParser()
        self.output_parser = OutputParser()
        self.planner = Planner(self.llm_client, self.prompt_builder)
        self.tool_executor = ToolExecutor(self.memory)
        self.loop = AgentLoop(self)

    def handle_request(self, message: str):
        """Processes a user message and returns the agent's response."""
        return self.loop.run_step(message)

if __name__ == "__main__":
    agent = CardKnowlogyAgent()
    response = agent.handle_request("I have chest pain and shortness of breath.")
    print(f"Agent Response: {response}")
