import logging
from typing import List, Dict, Any
import google.generativeai as genai
from config import Config
from document_processor import DocumentProcessor
from vector_store import VectorStore

logger = logging.getLogger(__name__)

class RAGChatbot:
    """RAG (Retrieval-Augmented Generation) Chatbot."""
    
    def __init__(self):
        """Initialize the RAG chatbot."""
        Config.validate()
        
        # Configure Gemini
        genai.configure(api_key=Config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
        
        # Initialize components
        self.document_processor = DocumentProcessor()
        self.vector_store = VectorStore()
        
        logger.info("RAG Chatbot initialized successfully")
    
    def load_documents(self, file_path: str):
        """
        Load and process documents into the vector store.
        
        Args:
            file_path (str): Path to the document file
        """
        try:
            logger.info(f"Loading documents from: {file_path}")
            
            # Process document
            text_chunks, embeddings = self.document_processor.process_document(file_path)
            
            # Store in vector database
            self.vector_store.add_documents(text_chunks, embeddings)
            
            logger.info("Documents loaded and indexed successfully")
            
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            raise
    
    def _retrieve_context(self, query: str, limit: int = None) -> str:
        """
        Retrieve relevant context for a query.
        
        Args:
            query (str): User query
            limit (int, optional): Number of results to retrieve
            
        Returns:
            str: Retrieved context
        """
        try:
            query_vector = self.document_processor.embed_query(query)
            
            # Search for relevant documents
            results = self.vector_store.search(query_vector, limit)
            
            context = "\\n\\n".join([result["text"] for result in results])
            
            return context
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            raise
    
    def _generate_response(self, query: str, context: str) -> str:
        """
        Generate response using Gemini.
        
        Args:
            query (str): User query
            context (str): Retrieved context
            
        Returns:
            str: Generated response
        """
        try:
            prompt = f"""You are a helpful assistant. Use the following context to answer the user's question accurately and concisely.

If you cannot find the answer in the context, say you don't know rather than making something up.

Context:
{context}

Question: {query}
Answer:"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise
    
    def chat(self, query: str) -> Dict[str, Any]:
        """
        Process a chat query and return response with metadata.
        
        Args:
            query (str): User query
            
        Returns:
            Dict[str, Any]: Response with metadata
        """
        try:
            logger.info(f"Processing query: {query}")
            
            context = self._retrieve_context(query)
            
            response = self._generate_response(query, context)
            
            logger.info("Query processed successfully")
            
            return {
                "query": query,
                "response": response,
                "context": context,
                "success": True
            }
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "query": query,
                "response": f"Sorry, I encountered an error: {str(e)}",
                "context": "",
                "success": False,
                "error": str(e)
            }
    
    def simple_chat(self, query: str) -> str:
        """
        Simple chat interface that returns just the response text.
        
        Args:
            query (str): User query
            
        Returns:
            str: Response text
        """
        result = self.chat(query)
        return result["response"]
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get chatbot status and collection info.
        
        Returns:
            Dict[str, Any]: Status information
        """
        try:
            collection_info = self.vector_store.get_collection_info()
            return {
                "status": "ready",
                "collection": collection_info,
                "model": Config.GEMINI_MODEL,
                "embedding_model": Config.EMBEDDING_MODEL
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }