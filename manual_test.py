import os
import sys
import json
from dotenv import load_dotenv

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_pipeline.pipeline_controller import handle_query

def main():
    load_dotenv()
    
    print("==================================================")
    print("Welcome to the NPS Saathi Manual Testing Console!")
    print("Type your question below.")
    print("Type 'exit' or 'quit' to close the console.")
    print("==================================================\n")
    
    # We use a default generic profile for testing intents
    default_profile = {
        "age": 30,
        "salary": 50000,
        "monthly_contribution": 5000,
        "risk_preference": "moderate",
        "years_of_service": 5,
        "government_employee": False,
        "retirement_age": 60,
        "expected_return": 0.10,
        "volatility": 0.15
    }

    while True:
        try:
            query = input("\n[You]: ")
            if query.lower() in ['exit', 'quit']:
                print("Exiting console. Goodbye!")
                break
                
            if not query.strip():
                continue
                
            print("\n[Thinking...]")
            
            # Send to the unified pipeline
            result = handle_query(query, default_profile)
            
            # Print the formatted response
            print("\n[NPS Saathi API Output]:")
            
            # Formatting the output nicely for the terminal
            print(f"Detected Intent : {result.get('intent')}")
            print(f"Response        : {result.get('response')}")
            
            if result.get('sources'):
                print(f"Sources Used    : {', '.join(result.get('sources'))}")
                
            if result.get('financial_data'):
                print("Financial Data attached (hidden for brevity).")
                
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nExiting console. Goodbye!")
            break
        except Exception as e:
            print(f"\n[Error]: {str(e)}")

if __name__ == "__main__":
    main()
