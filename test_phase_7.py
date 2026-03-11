import json
import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from decision_engine.recommendation_engine import (
    recommend_pension_scheme,
    recommend_monthly_contribution,
    recommend_asset_allocation,
    generate_financial_advice
)

def run_phase_7_tests():
    print("--- Starting Phase 7: Decision Intelligence Verification ---")

    user_profile = {
        "age": 30,
        "salary": 80000,
        "monthly_contribution": 5000,
        "risk_preference": "moderate",
        "years_of_service": 5,
        "government_employee": False
    }

    print("Test User Profile:")
    print(json.dumps(user_profile, indent=4))
    
    # Test Individual Modules
    print("\n[Test 1] Scheme Recommendation:")
    scheme = recommend_pension_scheme(user_profile)
    print(f"  Recommended: {scheme['recommended_scheme']}")
    print(f"  Reason: {scheme['reason']}")
    
    print("\n[Test 2] Asset Allocation:")
    allocation = recommend_asset_allocation(
        age=user_profile["age"], 
        risk_preference=user_profile["risk_preference"]
    )
    print(f"  Equity: {allocation['equity']}%")
    print(f"  Bonds: {allocation['bonds']}%")
    print(f"  Govt Securities: {allocation['government_securities']}%")
    
    print("\n[Test 3] Unified Financial Advice Output:")
    advice = generate_financial_advice(user_profile)
    print(json.dumps(advice, indent=4))
    
    # Verification Assertions
    assert "retirement_score" in advice, "Missing retirement score"
    assert advice["asset_allocation"]["equity"] + advice["asset_allocation"]["bonds"] + advice["asset_allocation"]["government_securities"] == 100, "Allocation must sum to 100"
    
    print("\n✅ Verification successful. The Decision Intelligence engine is functioning correctly!")

if __name__ == "__main__":
    run_phase_7_tests()
