"""Tenant-scoped vector store management."""
import os
from typing import List, Tuple

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings


class VectorStoreManager:
    def __init__(self, client_id: str, openai_api_key: str = None, store_path: str = "./data/vector_stores"):
        self.client_id = client_id
        self.store_path = os.path.join(store_path, client_id)
        self.vector_store = None
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=openai_api_key or os.getenv("OPENAI_API_KEY")
        )
        os.makedirs(self.store_path, exist_ok=True)

    def exists(self) -> bool:
        return os.path.exists(os.path.join(self.store_path, "index.faiss")) and os.path.exists(
            os.path.join(self.store_path, "index.pkl")
        )

    def create_vector_store(self, content: str, chunk_size: int = 1000) -> bool:
        """Create or replace the vector store for this tenant."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=200,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
        )
        chunks = text_splitter.split_text(content)
        if not chunks:
            return False

        self.vector_store = FAISS.from_texts(chunks, self.embeddings)
        self.save_vector_store()
        return True

    def similarity_search(self, query: str, k: int = 5) -> List:
        if not self.vector_store:
            self.load_vector_store()
        if self.vector_store:
            return self.vector_store.similarity_search(query, k=k)
        return []

    def similarity_search_with_score(self, query: str, k: int = 5) -> List[Tuple[object, float]]:
        """Return documents with FAISS distance scores for answerability decisions."""
        if not self.vector_store:
            self.load_vector_store()
        if self.vector_store:
            return self.vector_store.similarity_search_with_score(query, k=k)
        return []

    def save_vector_store(self) -> None:
        if self.vector_store:
            self.vector_store.save_local(self.store_path)

    def load_vector_store(self) -> bool:
        if not self.exists():
            return False
        try:
            self.vector_store = FAISS.load_local(
                self.store_path,
                self.embeddings,
                allow_dangerous_deserialization=True,
            )
            return True
        except Exception as exc:
            print(f"Error loading vector store for client {self.client_id}: {exc}")
            return False
