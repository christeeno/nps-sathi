import faiss
import numpy as np
import pickle
import os
from sentence_transformers import SentenceTransformer

# Initialize the embedding model (this will download weights on first run)
MODEL_NAME = "all-MiniLM-L6-v2"
embedding_model = SentenceTransformer(MODEL_NAME)

def generate_embeddings(chunks: list) -> tuple:
    """
    Generates embeddings for a list of chunk dictionaries.
    Returns:
        embeddings (numpy.ndarray): FAISS-compatible vectors
        metadata (list): Ordered list of chunk dictionaries
    """
    if not chunks:
        return np.array([]), []

    print(f"Generating embeddings for {len(chunks)} chunks using {MODEL_NAME}...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = embedding_model.encode(texts, show_progress_bar=True)
    
    # Normalize embeddings to improve search quality
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
    return np.array(embeddings).astype('float32'), chunks

def create_faiss_index(embeddings: np.ndarray, metadata: list, index_path: str, metadata_path: str):
    """
    Creates a FAISS index from embeddings and saves the index and metadata to disk.
    """
    if embeddings.size == 0:
        print("No embeddings to index.")
        return

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    
    # Save FAISS Index
    faiss.write_index(index, index_path)
    
    # Save Metadata mappings
    with open(metadata_path, "wb") as f:
        pickle.dump(metadata, f)
        
    print(f"Successfully saved FAISS index to {index_path} and metadata to {metadata_path}")

def load_faiss_index(index_path: str, metadata_path: str) -> tuple:
    """
    Loads a FAISS index and its corresponding metadata.
    """
    if not os.path.exists(index_path) or not os.path.exists(metadata_path):
        raise FileNotFoundError("FAISS index or metadata missing.")
        
    index = faiss.read_index(index_path)
    with open(metadata_path, "rb") as f:
        metadata = pickle.load(f)
    return index, metadata

def retrieve_context(query: str, index: faiss.Index, metadata: list, k: int = 5) -> list:
    """
    Retrieves the top-k most relevant chunks for a given query.
    """
    query_embedding = embedding_model.encode([query]).astype('float32')
    # Normalize query embedding for cosine similarity equivalent
    query_embedding = query_embedding / np.linalg.norm(query_embedding, axis=1, keepdims=True)
    
    distances, indices = index.search(query_embedding, k)
    
    results = []
    for score, idx in zip(distances[0], indices[0]):
        if idx != -1 and idx < len(metadata):
            results.append({
                "chunk": metadata[idx],
                "score": float(score)
            })
            
    return results
