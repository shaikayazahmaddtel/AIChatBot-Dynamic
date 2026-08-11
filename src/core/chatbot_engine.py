"""
Core Chatbot Engine
Main engine that processes conversations and generates responses
"""
from typing import Dict, List, Optional, Any
import json
from datetime import datetime
import hashlib
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferWindowMemory
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from .vector_store import VectorStoreManager
from .website_scraper import WebsiteScraper
from src.config.industry_prompts import INDUSTRY_PROMPTS

class ChatbotEngine:
    def __init__(self, client_id: str, config: Dict[str, Any]):
        self.client_id = client_id
        self.config = config
        self.industry = config.get('industry', 'general')
        self.conversation_stores = {}
        self.website_scraper = WebsiteScraper()
        self.vector_store_manager = VectorStoreManager(client_id)
        self._initialize_knowledge_base()
    
    def _initialize_knowledge_base(self):
        """Initialize knowledge base from website content"""
        try:
            website_url = self.config.get('website_url')
            if website_url:
                content = self.website_scraper.scrape_website(website_url)
                if content:
                    self.vector_store_manager.create_vector_store(content)
        except Exception as e:
            print(f"Error initializing knowledge base: {e}")
    
    def get_industry_prompt(self) -> str:
        """Get industry-specific prompt"""
        return INDUSTRY_PROMPTS.get(self.industry, INDUSTRY_PROMPTS['general'])
    
    def process_message(self, session_id: str, message: str, context: Optional[Dict] = None) -> Dict:
        """Process incoming message and return response"""
        try:
            if session_id not in self.conversation_stores:
                self.conversation_stores[session_id] = {
                    'memory': ConversationBufferWindowMemory(k=10, return_messages=True),
                    'messages': []
                }
            
            session = self.conversation_stores[session_id]
            
            # Create LLM
            llm = ChatOpenAI(
                temperature=0.7,
                model="gpt-3.5-turbo-16k",
                openai_api_key=self.config.get('openai_api_key')
            )
            
            # Get relevant context from vector store
            relevant_docs = self.vector_store_manager.similarity_search(message, k=3)
            context_str = "\n".join([doc.page_content for doc in relevant_docs])
            
            # Generate response
            system_prompt = self.get_industry_prompt()
            full_prompt = f"{system_prompt}\n\nRelevant context:\n{context_str}\n\nUser: {message}\nAssistant:"
            
            response = llm.predict(full_prompt)
            
            # Store message history
            session['messages'].append({
                'role': 'user',
                'content': message,
                'timestamp': datetime.now().isoformat()
            })
            session['messages'].append({
                'role': 'assistant',
                'content': response,
                'timestamp': datetime.now().isoformat()
            })
            
            return {
                'answer': response,
                'session_id': session_id,
                'sources': [{'content': doc.page_content[:200]} for doc in relevant_docs],
                'confidence': 0.85 if relevant_docs else 0.5
            }
            
        except Exception as e:
            return {
                'answer': "I apologize, but I encountered an error. Please try again.",
                'error': str(e),
                'session_id': session_id
            }
