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

def generate_rag_response(query: str, retrieved_chunks: list) -> str:
    """
    The main RAG pipeline generator.
    Formats the retrieved context, applies the strict prompt template, and invokes the LLM.
    """
    llm = get_llm()
    context_text = format_context(retrieved_chunks)
    
    # Format the prompt
    prompt_value = pension_prompt_template.invoke({
        "context_text": context_text,
        "query": query
    })
    
    # Generate the response
    response = llm.invoke(prompt_value)
    return response.content
