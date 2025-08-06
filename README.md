# RAG Tutorials

A collection of Retrieval-Augmented Generation (RAG) tutorials and examples using Qdrant vector database and modern AI models.

## Overview

This repository contains three (for now) comprehensive RAG implementations, from basic document Q&A to advanced agentic workflows. Each tutorial is designed for different skill levels and use cases.

## Tutorials
### Qdrant Setup & Tutorial
**Complete beginner's guide to Qdrant vector database**

Comprehensive tutorial materials for learning Qdrant from scratch, including setup guides and hands-on examples.

**What's Included:**
- Step-by-step installation (Docker and local)
- Interactive Jupyter notebook with real examples
- Performance insights and best practices
- AINS 3.0 conference materials

**Location:** `./AINS_qdrant_talk/`

**Best for:** Vector database beginners, Qdrant evaluation, educational workshops

### Simple RAG Chatbot
**Beginner-friendly implementation for quick starts**

A streamlined RAG chatbot that answers questions about your documents using Qdrant, Gemini AI, and Docling for document processing.

**Key Features:**
- Easy setup with minimal configuration
- Interactive chat interface
- Smart document chunking with BGE embeddings
- Support for PDF documents
- In-memory or persistent storage options

**Location:** `./qdrant_simple_rag/`

**Best for:** Personal document assistant, learning RAG basics, proof of concepts


### Agentic PDF RAG System
**Advanced implementation with intelligent document processing**

An intelligent document analysis system that combines PDF processing, vector search, and agentic AI workflows using LangGraph.

**Key Features:**
- GPT-4o vision for accurate text extraction from complex PDFs
- LangGraph-powered agent that makes smart retrieval decisions  
- Automatic document relevance evaluation
- Query rewriting for improved results
- Qdrant vector database with sub-24ms query latency

**Location:** `./Agentic-Qdrant-RAG/`

**Best for:** Research paper analysis, legal document review, complex document workflows






## Quick Start

### Simple RAG Chatbot (Recommended for beginners (the notebook ))

```bash
cd qdrant_simple_rag
pip install -r requirements.txt

# Add your API key to .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Run with your document
python main.py --document data/your_document.pdf
```

### Agentic RAG System (Advanced)

```bash
cd Agentic-Qdrant-RAG
pip install pypdfium2 backoff langchain-community langchain langchain-openai langgraph qdrant-client

# Set environment variables
export OPENAI_API_KEY="your-openai-key"
export QDRANT_API_KEY="your-qdrant-key"  # Optional for local setup
```

### Qdrant Tutorial

```bash
cd AINS_qdrant_talk
jupyter notebook Qdrant_talk.ipynb
```

Or run directly in [Google Colab](https://colab.research.google.com/drive/1TeZfj600xamgkM91B9mJphPAZ47F6mzC?usp=sharing)

## Technologies Used

- **Vector Database:** Qdrant for fast similarity search
- **Language Models:** GPT-4o, Google Gemini, Groq
- **Document Processing:** Docling, pypdfium2 for PDF handling
- **Embeddings:** BGE, OpenAI embeddings, Sentence Transformers
- **Frameworks:** LangChain, LangGraph for RAG workflows
- **Python Libraries:** FastEmbed, Transformers

## Repository Structure

```
├── Agentic-Qdrant-RAG/          # Advanced agentic RAG system
├── AINS_qdrant_talk/            # Qdrant tutorial and setup guide
├── qdrant_simple_rag/           # Simple RAG chatbot implementation
├── README.md
```

## Configuration

Required environment variables:

```bash
# For Gemini models
GEMINI_API_KEY=your_gemini_key

# For GPT-4o and OpenAI embeddings  
OPENAI_API_KEY=your_openai_key

# For Groq models
GROQ_API_KEY=your_groq_key

# Optional - for remote Qdrant
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
```

## Use Cases

**Enterprise Applications:**
- Legal document review and analysis
- Technical documentation Q&A
- Research paper analysis
- Customer support knowledge bases

**Educational & Research:**
- Academic paper analysis
- Interactive learning materials
- Literature review automation
- Cross-document research

**Personal Productivity:**
- Document assistant and note-taking
- Reading companion for books/articles
- Meeting notes summarization

## Featured Articles

- [Why Qdrant Will Be Your Favorite Vector Database](https://medium.com/@mohammedarbinsibi/why-qdrant-will-be-your-favorite-vector-database-setup-in-10-minutes-bc0a79651a14)
- [How I Built an Agentic RAG System with Qdrant](https://medium.com/@mohammedarbinsibi/how-i-built-an-agentic-rag-system-with-qdrant-to-chat-with-any-pdf-4f680e93397e)


## Coming Soon!

Will soon expanding these tutorials to cover more advanced techniques and integrations, including:

* Advanced RAG strategies (e.g., re-ranking, query expansion)
* Integration with other vector databases
* Deployment strategies for RAG systems

Stay tuned for updates!

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](contribution.md) for guidelines on how to contribute to this project.


## Contact

For questions or support, connect with [Mohamed Arbi Nsibi](https://www.linkedin.com/in/mohammed-arbi-nsibi-584a43241/) on LinkedIn.

## Acknowledgments

Special thanks to AINS 3.0 organizers and the open source community for making these tutorials possible.
