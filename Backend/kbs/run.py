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

def main():
    """
    Main autonomous loop for the CardKnowlogy AI Agent.
    Uses the full Agent core (LLM + Tools) to process input.
    """
    print("=== CardKnowlogy AI AGENT Started ===")
    print(f"Monitoring: {INPUT_FILE}")
    print(f"Results will be in: {OUTPUT_FILE}")
    print("Press Ctrl+C to stop.")

    # Initialize the Agent
    try:
        agent = CardKnowlogyAgent()
    except Exception as e:
        print(f"Error initializing AI Agent: {e}")
        return

    # Ensure data directory exists
    INPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Create input.json if it doesn't exist
    if not INPUT_FILE.exists():
        with open(INPUT_FILE, 'w') as f:
            f.write('{"message": "I have chest pain and shortness of breath."}')
        print(f"Created template input file at {INPUT_FILE}")

    while True:
        try:
            # 1. Check for input
            input_data = parse_input_file(INPUT_FILE)
            
            if input_data:
                print(f"\n[{time.strftime('%H:%M:%S')}] Detected input! AI Agent is thinking...")
                
                # Extract the message if it exists, otherwise use the whole JSON as context
                user_input = input_data.get("message")
                if not user_input:
                    # If it's a raw symptoms dict, convert it to a string for the agent
                    user_input = f"Diagnose this data: {input_data}"
                
                # 2. Run the AI Agent (which will call the KBS engine as a tool)
                result = agent.handle_request(user_input)
                
                # 3. Format and write output
                format_output_file(result, OUTPUT_FILE)
                
                # 4. Clear input to signify completion
                clear_input_file(INPUT_FILE)
                
                print(f"[{time.strftime('%H:%M:%S')}] Agent response saved. Waiting for next input.")
            
            # 5. Sleep to prevent high CPU usage
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\nShutting down agent...")
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            import traceback
            traceback.print_exc()
            time.sleep(5)

if __name__ == "__main__":
    main()
