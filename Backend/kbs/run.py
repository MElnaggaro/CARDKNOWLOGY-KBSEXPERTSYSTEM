import os
import sys
import time
from pathlib import Path

# Add the Backend directory to sys.path to allow imports to work correctly
BACKEND_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BACKEND_DIR))

from kbs.input.parser import parse_input_file, clear_input_file
from kbs.output.formatter import format_output_file
from ai_agent.core.agent import CardKnowlogyAgent

# Configuration
INPUT_FILE = BACKEND_DIR / "data" / "input.json"
OUTPUT_FILE = BACKEND_DIR / "data" / "output.json"

def print_pretty_result(result):
    """Prints the result in the beautiful style of test_engine.py"""
    print("\n" + "=" * 70)
    print("  DIAGNOSIS REPORT — CardKnowlogy AI Agent")
    print("=" * 70)
    
    # Handle Conversational Response
    if "message" in result:
        print(f"\n  [Agent Response]")
        print(f"  {result['message']}")
    
    # Handle Diagnostic Data (if KBS tool was used)
    if "primary_disease" in result:
        print("\n  [Diagnostic Results]")
        print("-" * 70)
        print(f"  Inferred Disease  : {result.get('primary_disease', 'None')}")
        print(f"  Confidence (CF)   : {result.get('confidence', 0.0)}")
        print(f"  Confidence Level  : {result.get('confidence_level', 'N/A')}")
        print(f"  Urgency Level     : {result.get('urgency', 'NORMAL')}")
        print(f"  Recommendation    : {result.get('recommendation', 'No specific recommendation.')}")
        
        print("\n  [Reasoning & Explanation]")
        print("-" * 70)
        explanation = result.get('explanation', {})
        fired_rules = explanation.get('fired_rules', [])
        print(f"  Fired Rules       : {', '.join(fired_rules) if fired_rules else 'None'}")
        
        key_facts = explanation.get('key_facts', [])
        if key_facts:
            print(f"  Key Facts         :")
            for fact in key_facts:
                print(f"    • {fact}")
                
        print(f"  Clinical Notes    : {explanation.get('clinical_notes', 'N/A')}")
        
    if "disclaimer" in result:
        print("\n" + "-" * 70)
        print(f"  DISCLAIMER: {result['disclaimer']}")
        
    # Memory Status (Persistent Data)
    print("\n  [Patient Memory Status]")
    print("-" * 70)
    print(f"  Status            : Data Kept (Persistent)")
    print(f"  Historical Facts  : {list(result.get('memory_snapshot', {}).keys()) if 'memory_snapshot' in result else 'All current symptoms preserved'}")
        
    print("\n" + "=" * 70 + "\n")

def main():
    """
    Main autonomous loop for the CardKnowlogy AI Agent.
    Prints professional reports to console and saves JSON to files.
    """
    print("=== CardKnowlogy AI AGENT Professional Mode ===")
    print(f"Monitoring: {INPUT_FILE}")
    print("Press Ctrl+C to stop.")

    # Initialize the Agent
    try:
        agent = CardKnowlogyAgent()
    except Exception as e:
        print(f"Error initializing AI Agent: {e}")
        return

    # Ensure data directory exists
    INPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    while True:
        try:
            # 1. Check for file-based input (Autonomous Mode)
            input_data = parse_input_file(INPUT_FILE)
            
            if input_data:
                print(f"\n[{time.strftime('%H:%M:%S')}] New file input detected! Thinking...")
                user_input = input_data.get("message")
                if not user_input:
                    user_input = f"Diagnose this data: {input_data}"
                
                # Run Agent
                result = agent.handle_request(user_input)
                print_pretty_result(result)
                
                format_output_file(result, OUTPUT_FILE)
                clear_input_file(INPUT_FILE)
            
            # 2. Support Interactive Mode (Manual Input)
            else:
                # Ask user if they want to enter something manually (optional)
                # To keep it from blocking file monitoring too much, we'll use a short timeout
                # or just provide a clear instruction.
                print(f"\n[{time.strftime('%H:%M:%S')}] Waiting for input.json or type your message here (or 'exit'):")
                user_input = input("> ").strip()
                
                if user_input.lower() in ['exit', 'quit']:
                    print("Shutting down agent...")
                    break
                
                if user_input:
                    # Run Agent
                    result = agent.handle_request(user_input)
                    print_pretty_result(result)
                    format_output_file(result, OUTPUT_FILE)

            time.sleep(1)
            
        except KeyboardInterrupt:
            print("\nShutting down agent...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(2)

if __name__ == "__main__":
    main()
