"""Tenant-aware RAG chatbot engine with website/general-knowledge fallback."""
import os
from datetime import datetime
from typing import Any, Dict, Optional

from langchain.memory import ConversationBufferWindowMemory
from langchain_openai import ChatOpenAI

from .vector_store import VectorStoreManager
from .website_scraper import WebsiteScraper
from src.config.industry_prompts import INDUSTRY_PROMPTS


class ChatbotEngine:
    def __init__(self, client_id: str, config: Dict[str, Any]):
        self.client_id = client_id
        self.config = config
        self.industry = config.get("industry", "general")
        self.conversation_stores: Dict[str, Dict[str, Any]] = {}
        self.website_scraper = WebsiteScraper()
        self.openai_api_key = config.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
        self.model = config.get("openai_model") or os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
        self.vector_store_manager = VectorStoreManager(client_id, self.openai_api_key)
        self._initialize_knowledge_base()

    def _initialize_knowledge_base(self) -> None:
        """Load an existing index first; only crawl when no index exists."""
        try:
            if self.vector_store_manager.exists():
                self.vector_store_manager.load_vector_store()
                return

            website_url = self.config.get("website_url")
            if website_url and self.openai_api_key:
                content = self.website_scraper.scrape_website(website_url)
                if content:
                    self.vector_store_manager.create_vector_store(content)
        except Exception as exc:
            print(f"Error initializing knowledge base for {self.client_id}: {exc}")

    def get_industry_prompt(self) -> str:
        return INDUSTRY_PROMPTS.get(self.industry, INDUSTRY_PROMPTS["general"])

    def _history_text(self, session: Dict[str, Any]) -> str:
        recent = session["messages"][-10:]
        return "\n".join(f"{item['role']}: {item['content']}" for item in recent)

    def process_message(self, session_id: str, message: str, context: Optional[Dict] = None) -> Dict:
        if not self.openai_api_key:
            return {
                "answer": "The chatbot AI provider is not configured for this customer.",
                "answer_type": "configuration_error",
                "session_id": session_id,
                "sources": [],
            }

        try:
            if session_id not in self.conversation_stores:
                self.conversation_stores[session_id] = {
                    "memory": ConversationBufferWindowMemory(k=10, return_messages=True),
                    "messages": [],
                }

            session = self.conversation_stores[session_id]
            relevant_docs = self.vector_store_manager.similarity_search(message, k=3)
            context_str = "\n\n".join(doc.page_content for doc in relevant_docs)
            history_str = self._history_text(session)

            llm = ChatOpenAI(
                temperature=0.2,
                model=self.model,
                openai_api_key=self.openai_api_key,
            )

            system_prompt = self.get_industry_prompt()
            if relevant_docs:
                answer_type = "website"
                instruction = (
                    "Answer using the website context when it contains the requested information. "
                    "Do not invent organization-specific facts. If the website context does not answer "
                    "the question, state that the website does not contain the information and then "
                    "provide a clearly labeled general-knowledge answer."
                )
            else:
                answer_type = "general"
                instruction = (
                    "The website knowledge base did not return relevant information. Clearly tell the "
                    "visitor that the website does not contain the requested information, then provide "
                    "a useful general-knowledge answer without presenting it as organization-specific."
                )

            full_prompt = f"""{system_prompt}

{instruction}

Website context:
{context_str or '(No relevant website content found)'}

Recent conversation:
{history_str or '(No previous messages)'}

Visitor: {message}
Assistant:"""

            response = llm.predict(full_prompt).strip()

            session["messages"].append({
                "role": "user",
                "content": message,
                "timestamp": datetime.now().isoformat(),
            })
            session["messages"].append({
                "role": "assistant",
                "content": response,
                "timestamp": datetime.now().isoformat(),
            })

            return {
                "answer": response,
                "answer_type": answer_type,
                "session_id": session_id,
                "sources": [
                    {"content": doc.page_content[:300]}
                    for doc in relevant_docs
                ],
                "confidence": min(0.95, 0.55 + (0.1 * len(relevant_docs))) if relevant_docs else 0.35,
            }
        except Exception as exc:
            return {
                "answer": "I apologize, but I encountered an error while processing your request.",
                "answer_type": "error",
                "error": str(exc),
                "session_id": session_id,
                "sources": [],
            }
