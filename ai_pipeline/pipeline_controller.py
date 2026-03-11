import logging
import os
import sys

# Ensure the project root is in sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_pipeline.intent_classifier import classify_intent
from ai_pipeline.response_formatter import format_response

# Import engines
from rag_engine.llm_interface import generate_rag_response
from rag_engine.vector_db import retrieve_context, load_faiss_index
from forecasting_engine.retirement_model import generate_retirement_forecast
from forecasting_engine.monte_carlo_simulator import run_monte_carlo_simulation
from decision_engine.recommendation_engine import generate_financial_advice

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load RAG resources once
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
FAISS_INDEX = os.path.join(DATA_DIR, 'vector_index.faiss')
METADATA_PKL = os.path.join(DATA_DIR, 'vector_metadata.pkl')

try:
    rag_index, rag_metadata = load_faiss_index(FAISS_INDEX, METADATA_PKL)
except Exception as e:
    logger.warning(f"Failed to load RAG index: {e}. Knowledge queries might fail.")
    rag_index, rag_metadata = None, None

def handle_query(query: str, user_profile: dict = None) -> dict:
    """
    Core orchestration module.
    Classifies intent, routes to the appropriate engine, and formats the output.
    """
    if user_profile is None:
        user_profile = {}
        
    # 1. Intent Classification
    intent = classify_intent(query)
    
    logger.info(f"Query: '{query}'")
    logger.info(f"Detected Intent: {intent}")
    
    # 2. Routing logic
    if intent == "knowledge_query":
        logger.info("Routing to: RAG Engine")
        
        if not rag_index:
            return format_response(intent, "Knowledge index is unavailable.")
            
        top_chunks = retrieve_context(query, rag_index, rag_metadata, k=3)
        rag_result = generate_rag_response(query, top_chunks)
        
        return format_response(
            intent=intent,
            response_text=rag_result.get("answer", ""),
            sources=rag_result.get("sources", [])
        )
        
    elif intent == "retirement_forecast":
        logger.info("Routing to: Forecasting Engine")
        forecast = generate_retirement_forecast(user_profile)
        
        response_text = f"Based on your profile, your projected corpus is ₹{forecast['projected_corpus']:,}. You can expect a monthly pension of ₹{forecast['monthly_pension']:,.2f} after investing ₹{forecast['annuity_investment']:,} in an annuity."
        
        return format_response(
            intent=intent,
            response_text=response_text,
            financial_data=forecast
        )
        
    elif intent == "simulation":
        logger.info("Routing to: Monte Carlo Simulator")
        age = user_profile.get("age", 30)
        retirement_age = user_profile.get("retirement_age", 60)
        monthly_contribution = user_profile.get("monthly_contribution", 5000)
        mean_return = user_profile.get("expected_return", 0.10)
        volatility = user_profile.get("volatility", 0.15)
        
        sim_results = run_monte_carlo_simulation(
            age=age,
            retirement_age=retirement_age,
            monthly_contribution=monthly_contribution,
            mean_return=mean_return,
            volatility=volatility,
            simulations=1000
        )
        
        response_text = f"Monte carlo simulation complete. Median corpus: ₹{sim_results['median_corpus']:,}. Best case: ₹{sim_results['best_case_corpus']:,}. Worst case: ₹{sim_results['worst_case_corpus']:,}."
        
        # Strip the full array for smaller payload
        financial_summary = {k: v for k, v in sim_results.items() if k != "all_simulations"}
        
        return format_response(
            intent=intent,
            response_text=response_text,
            financial_data=financial_summary
        )
        
    elif intent == "investment_recommendation":
        logger.info("Routing to: Decision Engine")
        advice = generate_financial_advice(user_profile)
        
        response_text = f"We recommend the {advice['recommended_scheme']} scheme. {advice['scheme_reason']} Your target asset allocation should be {advice['asset_allocation']['equity']}% Equity."
        
        return format_response(
            intent=intent,
            response_text=response_text,
            financial_data=advice
        )
        
    else:
        logger.info("Routing to: Fallback")
        return format_response("unknown", "I am unable to process this request.")
