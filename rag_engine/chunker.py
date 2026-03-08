import json
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_documents(documents: list, chunk_size: int = 500, chunk_overlap: int = 50) -> list:
    """
    Splits a list of LangChain documents into smaller semantic chunks.
    """
    if not documents:
        return []

    print(f"Chunking {len(documents)} documents (Size: {chunk_size}, Overlap: {chunk_overlap})...")
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " ", ""],
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    print(f"Created {len(chunks)} conceptual chunks.")
    return chunks

def save_chunks_to_json(chunks: list, output_path: str):
    """
    Saves document chunks to a JSON file for later use.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Serialize LangChain Documents into standard dicts with deterministic IDs
    serialized_chunks = []
    for i, chunk in enumerate(chunks):
        chunk_id = f"chunk_{i+1:04d}"
        source = chunk.metadata.get("source", "unknown")
        
        serialized_chunks.append({
            "chunk_id": chunk_id,
            "text": chunk.page_content,
            "source": source,
            "metadata": chunk.metadata
        })

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serialized_chunks, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully saved {len(chunks)} chunks to {output_path}")

def load_chunks_from_json(input_path: str) -> list:
    """
    Loads chunks from a JSON file.
    """
    if not os.path.exists(input_path):
        return []
    
    with open(input_path, "r", encoding="utf-8") as f:
        return json.load(f)
