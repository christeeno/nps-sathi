import re

def classify_intent(query: str) -> str:
    """
    Classifies the user query into one of the known engine intents using keyword heuristics.
    
    Intents:
    - knowledge_query
    - retirement_forecast
    - simulation
    - investment_recommendation
    """
    query_lower = query.lower()
    
    # Heuristics for investment recommendation (Decision Engine)
    if "recommend" in query_lower or "should i choose" in query_lower or "asset allocation" in query_lower or "nps vs ups" in query_lower or "nps or ups" in query_lower:
        return "investment_recommendation"
        
    # Heuristics for Monte Carlo simulation
    if "simulate" in query_lower or "monte carlo" in query_lower or "market crash" in query_lower or "worst case" in query_lower or "best case" in query_lower:
        return "simulation"
        
    # Heuristics for retirement forecast
    if "how much pension" in query_lower or "forecast" in query_lower or "projected corpus" in query_lower or "estimate my" in query_lower or "if i invest" in query_lower or "return" in query_lower and "pension" in query_lower:
        return "retirement_forecast"
        
    # Default to knowledge query (RAG Engine)
    return "knowledge_query"
