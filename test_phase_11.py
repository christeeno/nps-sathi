import json
from fastapi.testclient import TestClient
import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import app

client = TestClient(app)

def run_phase_11_tests():
    print("--- Starting Phase 11: API Backend Verification ---")
    
    # Base Profile for tests
    profile_payload = {
        "age": 30,
        "salary": 80000,
        "monthly_contribution": 5000,
        "risk_preference": "moderate",
        "years_of_service": 5,
        "government_employee": False,
        "retirement_age": 60,
        "expected_return": 0.10,
        "volatility": 0.15
    }

    # Test 1: GET /
    print("\n[Test 1] GET / (Health Check)")
    response = client.get("/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200

    # Test 2: POST /api/v1/ask
    print("\n[Test 2] POST /api/v1/ask  (Query Routing)")
    ask_payload = {
        "query": "Should I choose NPS or UPS?",
        "user_profile": profile_payload
    }
    response = client.post("/api/v1/ask", json=ask_payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200
    assert response.json()["intent"] == "investment_recommendation"

    # Test 3: POST /api/v1/forecast
    print("\n[Test 3] POST /api/v1/forecast")
    response = client.post("/api/v1/forecast", json=profile_payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200
    assert "projected_corpus" in response.json()

    # Test 4: POST /api/v1/simulate
    print("\n[Test 4] POST /api/v1/simulate")
    response = client.post("/api/v1/simulate", json=profile_payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200
    assert "median_corpus" in response.json()

    # Test 5: POST /api/v1/recommend
    print("\n[Test 5] POST /api/v1/recommend")
    response = client.post("/api/v1/recommend", json=profile_payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200
    assert "recommended_scheme" in response.json()
    
    print("\n✅ Verification successful. The FastAPI REST endpoints are fully functional!")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    run_phase_11_tests()
