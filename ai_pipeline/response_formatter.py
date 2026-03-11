from typing import List, Dict, Any

def format_response(intent: str, response_text: str = "", sources: List[str] = None, financial_data: Dict[str, Any] = None) -> dict:
    """
    Normalizes outputs from different engines into a unified structure.
    """
    if sources is None:
        sources = []
    if financial_data is None:
        financial_data = {}
        
    return {
        "intent": intent,
        "response": response_text,
        "sources": sources,
        "financial_data": financial_data
    }
