"""
Vector Store Manager for Embedding Storage
"""
import os
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

class VectorStoreManager:
    def __init__(self, client_id: str, store_path: str = './data/vector_stores'):
        self.client_id = client_id
        self.store_path = os.path.join(store_path, client_id)
        self.vector_store = None
        self.embeddings = OpenAIEmbeddings()
        os.makedirs(self.store_path, exist_ok=True)
    
    def create_vector_store(self, content: str, chunk_size: int = 1000):
        """Create vector store from content"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        chunks = text_splitter.split_text(content)
        
        if chunks:
            self.vector_store = FAISS.from_texts(chunks, self.embeddings)
            self.save_vector_store()
    
    def similarity_search(self, query: str, k: int = 5) -> List:
        """Search for similar documents"""
        if not self.vector_store:
            self.load_vector_store()
        
        if self.vector_store:
            return self.vector_store.similarity_search(query, k=k)
        return []
    
    def save_vector_store(self):
        """Save vector store to disk"""
        if self.vector_store:
            self.vector_store.save_local(self.store_path)
    
    def load_vector_store(self):
        """Load vector store from disk"""
        try:
            if os.path.exists(self.store_path):
                self.vector_store = FAISS.load_local(
                    self.store_path, 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
        except Exception as e:
            print(f"Error loading vector store: {e}")
