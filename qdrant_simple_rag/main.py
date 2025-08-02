
import argparse
import logging
import sys
import os
from pathlib import Path
from chatbot import RAGChatbot
from config import Config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_environment():
    """Setup the environment and check for required files."""
    env_file = Path('.env')
    if not env_file.exists():
        print("Creating .env file template...")
        with open('.env', 'w') as f:
            f.write("# Add your Gemini API key here\n")
            f.write("GEMINI_API_KEY=your_api_key_here\n")
        print("Please add your GEMINI_API_KEY to the .env file and run again.")
        return False
    
    return True

def interactive_mode(chatbot: RAGChatbot):
    """Run the chatbot in interactive mode."""
    print("\\n RAG Chatbot is ready! Type 'quit', 'exit', or 'q' to exit.")
    print("Commands:")
    print("  status - Show chatbot status")
    print("  help - Show this help message")
    print("-" * 50)
    
    while True:
        try:
            query = input("\\n👤 You: ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['quit', 'exit', 'q']:
                print("\\n👋 Goodbye!")
                break
            elif query.lower() == 'status':
                status = chatbot.get_status()
                print(f"\\n Status: {status}")
                continue
            elif query.lower() == 'help':
                print("\\n Available commands:")
                print("  status - Show chatbot status")
                print("  help - Show this help message")
                print("  quit/exit/q - Exit the chatbot")
                continue
            
            print("\\n🤖 Bot: ", end="", flush=True)
            response = chatbot.simple_chat(query)
            print(response)
            
        except KeyboardInterrupt:
            print("\\n\\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\\n❌ Error: {e}")

def single_query_mode(chatbot: RAGChatbot, query: str):
    """Run a single query and exit."""
    try:
        response = chatbot.simple_chat(query)
        print(f"Query: {query}")
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="RAG Chatbot with Qdrant, Gemma3, and Docling")
    parser.add_argument(
        "--document", 
        "-d", 
        help="Path to document to load", 
        default=Config.DEFAULT_DOCUMENT_PATH
    )
    parser.add_argument(
        "--query", 
        "-q", 
        help="Single query to run (non-interactive mode)"
    )
    parser.add_argument(
        "--verbose", 
        "-v", 
        action="store_true", 
        help="Enable verbose logging"
    )
    parser.add_argument(
        "--setup", 
        action="store_true", 
        help="Setup environment and exit"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    if args.setup:
        setup_environment()
        return
    
    if not setup_environment():
        sys.exit(1)
    
    try:
        # Initialize chatbot
        print("🚀 Initializing RAG Chatbot...")
        chatbot = RAGChatbot()
        
        document_path = Path(args.document)
        if not document_path.exists():
            print(f"❌ Document not found: {args.document}")
            print(f"Please provide a valid document path using --document or place your document at {Config.DEFAULT_DOCUMENT_PATH}")
            sys.exit(1)
        
        print(f" Loading document: {args.document}")
        chatbot.load_documents(str(document_path))
        
        # Show status
        status = chatbot.get_status()
        print(f"✅ Chatbot ready! Collection has {status.get('collection', {}).get('vectors_count', 0)} documents")
        
        if args.query:
            single_query_mode(chatbot, args.query)
        else:
            interactive_mode(chatbot)
            
    except KeyboardInterrupt:
        print("\\n\\n👋 Goodbye!")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()