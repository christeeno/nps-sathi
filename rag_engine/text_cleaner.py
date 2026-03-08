import re

def clean_text(text: str) -> str:
    """
    Cleans raw document text by removing excess whitespace, newlines, and non-printable characters.
    """
    if not text:
        return ""

    # Replace multiple newlines with a single space
    text = re.sub(r'\n+', ' ', text)
    
    # Replace multiple spaces/tabs with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading and trailing whitespace
    text = text.strip()
    
    return text

def clean_documents(documents: list) -> list:
    """
    Applies text cleaning to a list of LangChain Document objects.
    """
    for doc in documents:
        doc.page_content = clean_text(doc.page_content)
    return documents
