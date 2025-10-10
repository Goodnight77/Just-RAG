"""Core models and processing logic for Bolt RAG."""

import os
import tempfile
from pathlib import Path
import base64
import warnings

from langchain_community.document_loaders import PyPDFLoader
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_cohere import CohereEmbeddings
from langchain_groq import ChatGroq
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

from config import Config

warnings.filterwarnings("ignore", message=".*torch.classes.*")


def get_embeddings():
    """Cohere embeddings model."""
    return CohereEmbeddings(
        model=Config.EMBEDDING_MODEL, cohere_api_key=Config.COHERE_API_KEY
    )


def get_llm():
    """Initialize and return Groq LLM."""
    return ChatGroq(
        groq_api_key=Config.GROQ_API_KEY,
        model_name=Config.LLM_MODEL,
        temperature=Config.LLM_TEMPERATURE,
    )


def get_logo_data_uri():
    logo_path = Path(__file__).with_name("img/logomark.svg")
    try:
        with open(logo_path, "rb") as fh:
            encoded = base64.b64encode(fh.read()).decode("utf-8")
        return f"data:image/svg+xml;base64,{encoded}"
    except OSError:
        return ""


def process_pdfs(files, embeddings, collection_name):
    """
    Process uploaded PDF files and create a vector store.

    Args:
        files: List of uploaded PDF files
        embeddings: Embedding model instance
        collection_name: Name for the Qdrant collection

    Returns:
        QdrantVectorStore instance
    """
    print(f"[DEBUG] Processing {len(files)} PDF file(s)")
    print(f"[DEBUG] Collection name: {collection_name}")

    docs = []
    for f in files:
        print(f"[DEBUG] Loading file: {f.name}")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(f.getvalue())
            path = tmp.name
        docs += RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE, chunk_overlap=Config.CHUNK_OVERLAP
        ).split_documents(PyPDFLoader(path).load())
        os.unlink(path)

    print(f"[DEBUG] Total chunks created: {len(docs)}")

    # Create vector store from documents using in-memory location
    vector_store = QdrantVectorStore.from_documents(
        docs,
        embeddings,
        location=":memory:",
        collection_name=collection_name,
    )
    print("[DEBUG] Vector store created successfully")
    return vector_store


def build_chain(vs, llm):
    """
    Build a conversational retrieval chain.

    Args:
        vs: Vector store instance
        llm: Language model instance

    Returns:
        ConversationalRetrievalChain instance
    """
    prompt = PromptTemplate(
        template=Config.PROMPT_TEMPLATE,
        input_variables=["context", "chat_history", "question"],
    )
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return ConversationalRetrievalChain.from_llm(
        llm,
        retriever=vs.as_retriever(search_kwargs={"k": Config.RETRIEVAL_K}),
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
    )
