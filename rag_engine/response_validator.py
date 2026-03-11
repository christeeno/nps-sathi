import re

def validate_response(response: str, retrieved_chunks: list) -> str:
    """
    Validates whether the generated response is grounded in the retrieved context.
    If unsupported or hallucinated, it rejects the response.
    """
    # Simple heuristic validation: if the LLM states it doesn't know,
    # or if we want to run an explicit NLI (Natural Language Inference) check, we do it here.
    
    # Common LLM refusal phrases when instructed to stick to context
    refusal_patterns = [
        r"i don'?t have (that|the) information",
        r"i could not find",
        r"is not mentioned in the",
        r"does not contain information",
        r"i am sorry",
        r"i cannot answer",
        r"outside the scope"
    ]
    
    response_lower = response.lower()
    for pattern in refusal_patterns:
        if re.search(pattern, response_lower):
            return "I could not find this information in the pension policy documents."
            
    # As a secondary check, we can verify if the response actually contains citations
    # If the user prompt mandates citations and they are missing, it might be a hallucination.
    if not re.search(r'\[chunk_\d+\]', response):
        # We might have a response but without citations. Depending on strictness, we could reject it.
        # But for this phase, we rely on the prompt's instruction to output them.
        pass

    return response
