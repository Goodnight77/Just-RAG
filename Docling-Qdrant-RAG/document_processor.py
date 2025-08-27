
import logging
from typing import List, Tuple
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker
from fastembed import TextEmbedding
from config import Config

logger = logging.getLogger(__name__)

class DocumentProcessor:
    """Handles document loading, chunking, and embedding."""
    
    def __init__(self):
        """Initialize the document processor."""
        self.embedding_model = TextEmbedding(model_name=Config.EMBEDDING_MODEL)
        self.chunker = HybridChunker(tokenizer=Config.CHUNK_TOKENIZER)
        logger.info(f"Initialized DocumentProcessor with embedding model: {Config.EMBEDDING_MODEL}")
    
    def load_document(self, file_path: str):
        """
        Load and convert a document using Docling.
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            Document: Processed document object
        """
        try:
            logger.info(f"Loading document from: {file_path}")
            converter = DocumentConverter()
            result = converter.convert(source=file_path)
            logger.info("Document loaded successfully")
            return result.document
        except Exception as e:
            logger.error(f"Error loading document: {e}")
            raise
    
    def chunk_document(self, document) -> List[str]:
        """
        Chunk the document into smaller pieces.
        
        Args:
            document: Document object from Docling
            
        Returns:
            List[str]: List of text chunks
        """
        try:
            logger.info(f"Chunking document with max_tokens: {Config.MAX_TOKENS}")
            chunks = self.chunker.chunk(dl_doc=document, max_tokens=Config.MAX_TOKENS)
            text_chunks = [chunk.text for chunk in chunks]
            logger.info(f"Document chunked into {len(text_chunks)} pieces")
            return text_chunks
        except Exception as e:
            logger.error(f"Error chunking document: {e}")
            raise
    
    def generate_embeddings(self, text_chunks: List[str]) -> List[List[float]]:
        """
        Generate embeddings for text chunks.
        
        Args:
            text_chunks (List[str]): List of text chunks
            
        Returns:
            List[List[float]]: List of embedding vectors
        """
        try:
            logger.info(f"Generating embeddings for {len(text_chunks)} chunks")
            embeddings = list(self.embedding_model.embed(text_chunks))
            logger.info(f"Generated {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise
    
    def process_document(self, file_path: str) -> Tuple[List[str], List[List[float]]]:
        """
        Complete document processing pipeline.
        
        Args:
            file_path (str): Path to the document file
            
        Returns:
            Tuple[List[str], List[List[float]]]: Text chunks and their embeddings
        """
        document = self.load_document(file_path)
        text_chunks = self.chunk_document(document)
        embeddings = self.generate_embeddings(text_chunks)
        
        return text_chunks, embeddings
    
    def embed_query(self, query_text: str) -> List[float]:
        """
        Generate embedding for a query.
        
        Args:
            query_text (str): Query text
            
        Returns:
            List[float]: Query embedding vector
        """
        try:
            embedding = list(self.embedding_model.embed([query_text]))[0]
            return embedding
        except Exception as e:
            logger.error(f"Error embedding query: {e}")
            raise