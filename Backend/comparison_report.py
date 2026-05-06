import sys
import os
import json
from pathlib import Path

# Add Backend to path
BACKEND_DIR = Path(__file__).parent
sys.path.insert(0, str(BACKEND_DIR))

from kbs.engine.runner import run_diagnosis
from ai_agent.core.agent import CardKnowlogyAgent

def compare_outputs():
    print("=" * 80)
    print("      KBS vs AI AGENT COMPARISON REPORT")
    print("=" * 80)

    # Sample data: Chest pain and shortness of breath
    test_inputs = {
        "symptoms": {
            "chest_pain": True,
            "shortness_of_breath": True
        },
        "vitals": {},
        "background": {}
    }
    
    user_message = "I have chest pain and I am struggling to breathe."

    print(f"\n[Test Case]: {user_message}")
    print("-" * 80)

    # 1. Run RAW KBS
    print("\n[1] RAW KBS Output (Rule-based only):")
    kbs_result = run_diagnosis(test_inputs)
    print(f"  - Disease Identified: {kbs_result.get('primary_disease')}")
    print(f"  - Confidence (CF): {kbs_result.get('confidence')}")
    print(f"  - Recommendation: {kbs_result.get('recommendation')[:50]}...")

    # 2. Run AI AGENT
    print("\n[2] AI AGENT Output (Reasoning + Memory + KBS):")
    agent = CardKnowlogyAgent()
    agent_result = agent.handle_request(user_message)
    
    print(f"  - Conversational Message: {agent_result.get('message', 'N/A')}")
    print(f"  - Primary Disease: {agent_result.get('primary_disease')}")
    print(f"  - Confidence: {agent_result.get('confidence')}")
    print(f"  - Memory Status: { 'Data Kept Persistent' if 'memory_snapshot' in agent_result else 'None'}")
    
    print("\n" + "-" * 80)
    print("ANALYSIS:")
    print("- The Raw KBS provides a structured diagnosis based strictly on rules.")
    print("- The AI Agent wraps the KBS result in a natural language explanation, ")
    print("  remembers patient history (Memory), and can ask clarifying questions.")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    compare_outputs()
