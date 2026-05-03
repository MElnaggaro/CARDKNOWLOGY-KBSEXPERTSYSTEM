import json
import re

class OutputParser:
    """Parses LLM output into structured agent actions."""
    
    @staticmethod
    def parse_llm_action(response: str) -> dict:
        """
        Expects LLM to return a JSON block or a specific format.
        Example:
        {
            "action": "call_kbs",
            "parameters": {"symptoms": {"chest_pain": true}}
        }
        """
        try:
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            return {"action": "speak", "parameters": {"message": response}}
        except Exception:
            return {"action": "error", "parameters": {"message": "Failed to parse agent action"}}
