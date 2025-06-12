from dotenv import load_dotenv
import streamlit as st

from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.vectorstores import Qdrant
from langchain.embeddings.openai import OpenAIEmbeddings
import qdrant_client
import os
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

def get_vector_store():
    
    client = qdrant_client.QdrantClient(
        os.getenv("QDRANT_HOST"),
        api_key=os.getenv("QDRANT_API_KEY")
    )
    
    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


    vector_store = Qdrant(
        client=client, 
        collection_name=os.getenv("QDRANT_COLLECTION_NAME"), 
        embeddings=embeddings,
    )
    
    return vector_store
from langchain_groq import ChatGroq

def main():
    load_dotenv()
    
    st.set_page_config(page_title="Ask Qdrant")
    st.header("Ask your remote database 💬")
    
    # create vector store
    vector_store = get_vector_store()
    
    # create chain 
    qa = RetrievalQA.from_chain_type(
        llm = ChatGroq(
                temperature=0,
                model= "llama-3.3-70b-versatile", #"llama-3.1-70b-versatile", #"llama3-70b-8192",
                api_key="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",),

        chain_type="stuff",
        retriever=vector_store.as_retriever()
    )

    # show user input
    user_question = st.text_input("Ask a question about your CV:")
    if user_question:
        st.write(f"Question: {user_question}")
        answer = qa.run(user_question)
        st.write(f"Answer: {answer}")
    
        
if __name__ == '__main__':
    main()
