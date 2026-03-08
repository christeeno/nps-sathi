import os
from langchain_community.document_loaders import PyPDFDirectoryLoader, DirectoryLoader, TextLoader

def load_documents(directory_path: str) -> list:
    """
    Loads PDF and Text documents from a given directory.
    Returns a list of LangChain Document objects.
    """
    if not os.path.exists(directory_path):
        print(f"Warning: Directory '{directory_path}' does not exist. Returning empty list.")
        return []

    documents = []

    # Load PDFs
    print(f"Loading PDFs from {directory_path}...")
    pdf_loader = PyPDFDirectoryLoader(directory_path)
    pdf_docs = pdf_loader.load()
    documents.extend(pdf_docs)
    print(f"Loaded {len(pdf_docs)} PDF pages.")

    # Load TXT files
    print(f"Loading TXT files from {directory_path}...")
    txt_loader = DirectoryLoader(directory_path, glob="**/*.txt", loader_cls=TextLoader)
    txt_docs = txt_loader.load()
    documents.extend(txt_docs)
    print(f"Loaded {len(txt_docs)} TXT files.")

    return documents
