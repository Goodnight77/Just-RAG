import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the RAG chatbot."""
    
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"
    CHUNK_TOKENIZER = "sentence-transformers/all-MiniLM-L6-v2"
    GEMINI_MODEL = "gemma-3-27b-it"
    
    # Chunking parameters
    MAX_TOKENS = 256
    
    # Vector store settings
    COLLECTION_NAME = "rust-book"
    QDRANT_URL = ":memory:"  # Use ":memory:" for in-memory, or provide URL for persistent storage
    
    # Search parameters
    RETRIEVAL_LIMIT = 3
    
    # Default document path
    DEFAULT_DOCUMENT_PATH = "data/the_rust_workbook.pdf"
    
    @classmethod
    def validate(cls):
        """Validate that required configuration is present."""
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY environment variable is required. Please set it in your .env file.")
        
        return True