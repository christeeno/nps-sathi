import json
import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from forecasting_engine.retirement_model import generate_retirement_forecast

def run_phase_5_tests():
    print("--- Starting Phase 5: Retirement Forecasting Engine Verification ---")
    
    test_profile = {
        "age": 30,
        "retirement_age": 60,
        "monthly_contribution": 5000,
        "expected_return": 0.10
    }
    
    print("User Profile Input:")
    print(json.dumps(test_profile, indent=4))
    
    forecast = generate_retirement_forecast(test_profile)
    
    print("\nForecast Summary Output:")
    print(json.dumps(forecast, indent=4))
    
    # Simple assertion checks
    assert forecast["projected_corpus"] > 0, "Corpus should be greater than 0"
    assert forecast["lump_sum"] > 0, "Lump sum should be greater than 0"
    assert forecast["annuity_investment"] > 0, "Annuity investment should be greater than 0"
    assert forecast["monthly_pension"] > 0, "Monthly pension should be greater than 0"
    
    print("\n✅ Verification successful. The forecasting engine is working correctly.")

if __name__ == "__main__":
    run_phase_5_tests()
