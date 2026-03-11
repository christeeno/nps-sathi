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
    
    choice = input("Would you like to use the default user profile or enter a custom one? (default/custom) [default]: ").strip().lower()
    if choice == 'custom':
        print("\n--- Enter Custom Profile ---")
        try:
            profile = {
                "age": int(input("Age (e.g. 30) [30]: ") or 30),
                "salary": float(input("Monthly Salary (e.g. 50000) [50000]: ") or 50000),
                "monthly_contribution": float(input("Monthly Contribution (e.g. 5000) [5000]: ") or 5000),
                "risk_preference": (input("Risk Preference (low/moderate/high) [moderate]: ") or "moderate").strip(),
                "years_of_service": int(input("Years of Service (e.g. 5) [5]: ") or 5),
                "government_employee": input("Government Employee? (y/N): ").strip().lower() == 'y',
                "retirement_age": int(input("Retirement Age (e.g. 60) [60]: ") or 60),
                "expected_return": float(input("Expected Annual Return (e.g. 0.10) [0.10]: ") or 0.10),
                "volatility": float(input("Volatility (e.g. 0.15) [0.15]: ") or 0.15)
            }
        except ValueError:
            print("Invalid input detected. Falling back to default profile.")
            profile = {"age": 30, "salary": 50000, "monthly_contribution": 5000, "risk_preference": "moderate", "years_of_service": 5, "government_employee": False, "retirement_age": 60, "expected_return": 0.10, "volatility": 0.15}
        print("----------------------------\n")
    else:
        profile = {
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
            result = handle_query(query, profile)
            
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
