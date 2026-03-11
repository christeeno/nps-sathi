import os
try:
    from langchain_openai import ChatOpenAI
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    pass

from .prompt_templates import pension_prompt_template
from .vector_db import retrieve_context

def get_llm():
    """
    Initializes the LLM based on available environment variables.
    Currently prioritizes Google Gemini, falling back to OpenAI.
    """
    if os.getenv("GOOGLE_API_KEY"):
        print("Using Google Gemini 2.5 Flash...")
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
    elif os.getenv("OPENAI_API_KEY"):
        print("Using OpenAI GPT-4o-mini...")
        return ChatOpenAI(model="gpt-4o-mini", temperature=0)
    else:
        raise ValueError("No LLM API key found in environment variables. Please set GOOGLE_API_KEY or OPENAI_API_KEY.")

def format_context(retrieved_chunks: list, max_tokens: int = 1200) -> str:
    """
    Formats the context efficiently, injecting source and chunk_id metadata 
    to ensure the LLM can provide correct citations. Limits tokens roughly.
    """
    formatted_chunks = []
    estimated_length = 0
    
    for res in retrieved_chunks:
        chunk = res["chunk"]
        chunk_text = f"[{chunk.get('chunk_id')} | source: {chunk.get('source')}]\n{chunk.get('text')}"
        
        # Rough token estimation (1 token approx 4 chars)
        if estimated_length + (len(chunk_text) / 4) > max_tokens:
            break
            
        formatted_chunks.append(chunk_text)
        estimated_length += len(chunk_text) / 4
        
    return "\n\n".join(formatted_chunks)

import json
from .response_validator import validate_response

def generate_rag_response(query: str, retrieved_chunks: list) -> dict:
    """
    The main RAG pipeline generator with hallucination prevention.
    Formats the retrieved context, applies the strict prompt template, invokes the LLM,
    and then parses and validates the response securely.
    """
    if not retrieved_chunks:
        return {
            "answer": "This question is outside the scope of pension policy documents.",
            "sources": []
        }
    
    llm = get_llm()
    context_text = format_context(retrieved_chunks)
    
    # Format the prompt
    prompt_value = pension_prompt_template.invoke({
        "context_text": context_text,
        "query": query
    })
    
    # Generate the response
    llm_output = llm.invoke(prompt_value).content
    
    # Parse the LLM output (expecting JSON)
    try:
        # Strip markdown json block if LLM added it
        raw_json = llm_output.strip()
        if raw_json.startswith("```json"):
            raw_json = raw_json[7:-3].strip()
        elif raw_json.startswith("```"):
            raw_json = raw_json[3:-3].strip()
            
        parsed_response = json.loads(raw_json)
        answer = parsed_response.get("answer", "")
        sources = parsed_response.get("sources", [])
        
    except json.JSONDecodeError:
        # Fallback if the LLM didn't return strict JSON
        answer = llm_output
        sources = []
        
    # Validate the semantic answer against rules
    validated_answer = validate_response(answer, retrieved_chunks)
    
    # If the validator overwrote it with the rejection phrase, clear the sources
    if validated_answer == "I could not find this information in the pension policy documents.":
        sources = []
        
    return {
        "answer": validated_answer,
        "sources": sources
    }
