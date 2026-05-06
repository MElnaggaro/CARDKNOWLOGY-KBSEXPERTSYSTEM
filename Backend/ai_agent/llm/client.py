import os
import json
from ..config import settings

class LLMClient:
    """Interface for LLM calls (OpenAI, Local, etc.)."""
    
    def __init__(self, provider: str = "openai"):
        self.provider = provider
        self.api_key = settings.OPENAI_API_KEY
        self.client = None
        
        if self.api_key and self.api_key != "your_openai_api_key_here":
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except ImportError:
                print("WARNING: openai library not installed. Falling back to Mock.")

    def complete(self, prompt: str, system_prompt: str = "") -> str:
        """Sends a prompt to the LLM and returns the response."""
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model=settings.MODEL_NAME,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"}
                )
                return response.choices[0].message.content
            except Exception as e:
                return json.dumps({"action": "error", "parameters": {"message": f"LLM Error: {str(e)}"}})

        # Smart Mock Logic for demonstration
        print(f"DEBUG: [Mock LLM] Processing assessment request...")
        
        prompt_lower = prompt.lower()
        
        # Check if we should call the KBS for assessment
        if any(word in prompt_lower for word in ["chest pain", "breath", "fever", "cough", "fatigue", "diagnose", "assess"]):
            # Extract symptoms from prompt (very basic extraction)
            symptoms = {
                "chest_pain": "chest pain" in prompt_lower,
                "shortness_of_breath": "breath" in prompt_lower,
                "fever": "fever" in prompt_lower,
                "cough": "cough" in prompt_lower
            }
            # Remove False values to keep it clean
            symptoms = {k: v for k, v in symptoms.items() if v}
            
            return json.dumps({
                "action": "call_kbs",
                "parameters": {
                    "symptoms": symptoms
                }
            })
            
        # Default conversational response
        return json.dumps({
            "action": "speak",
            "parameters": {"message": "I am the CardKnowlogy AI Agent. I can help assess your symptoms and keep track of your medical history without 'learning' from it (maintaining your privacy and data integrity)."}
        })
