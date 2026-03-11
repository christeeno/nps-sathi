from fastapi import APIRouter, HTTPException
import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.schemas import QueryRequest, UserProfile
from ai_pipeline.pipeline_controller import handle_query
from forecasting_engine.retirement_model import generate_retirement_forecast
from forecasting_engine.monte_carlo_simulator import run_monte_carlo_simulation
from decision_engine.recommendation_engine import generate_financial_advice

router = APIRouter(prefix="/api/v1")

@router.post("/ask", summary="Send a unified AI Query")
async def ask_ai(request: QueryRequest):
    """
    Routes a general text query through the AI Pipeline Controller.
    """
    user_profile_dict = request.user_profile.model_dump() if request.user_profile else {}
    
    try:
        response = handle_query(request.query, user_profile_dict)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/forecast", summary="Generate a deterministic retirement forecast")
async def forecast_endpoint(profile: UserProfile):
    """
    Directly calls the forecasting engine using the provided profile.
    """
    try:
        result = generate_retirement_forecast(profile.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/simulate", summary="Run a Monte Carlo retirement simulation")
async def simulate_endpoint(profile: UserProfile):
    """
    Directly calls the Monte Carlo stochastic engine.
    """
    try:
        data = profile.model_dump()
        result = run_monte_carlo_simulation(
            age=data["age"],
            retirement_age=data["retirement_age"],
            monthly_contribution=data["monthly_contribution"],
            mean_return=data["expected_return"],
            volatility=data["volatility"]
        )
        # Strip exact list for JSON payload stability
        summary = {k: v for k, v in result.items() if k != "all_simulations"}
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/recommend", summary="Generate financial advice and schemes")
async def recommend_endpoint(profile: UserProfile):
    """
    Directly calls the Decision Intelligence engine.
    """
    try:
        result = generate_financial_advice(profile.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
