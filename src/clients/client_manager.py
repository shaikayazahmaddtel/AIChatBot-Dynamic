"""
Multi-Client Management System
"""
import json
import uuid
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import redis

class ClientManager:
    def __init__(self, redis_client: redis.Redis = None):
        self.clients = {}
        self.redis = redis_client or redis.from_url('redis://localhost:6379')
    
    def register_client(self, client_data: Dict) -> Dict:
        """Register a new client"""
        client_id = str(uuid.uuid4())
        api_key = f"sk-{uuid.uuid4().hex}"
        
        client = {
            'client_id': client_id,
            'name': client_data['name'],
            'industry': client_data['industry'],
            'website_url': client_data['website_url'],
            'api_key': api_key,
            'openai_api_key': client_data.get('openai_api_key'),
            'plan': client_data.get('plan', 'basic'),
            'max_tokens_per_day': client_data.get('max_tokens_per_day', 100000),
            'status': 'active',
            'created_at': datetime.now().isoformat()
        }
        
        # Store in Redis
        self.redis.setex(
            f"client:{client_id}",
            timedelta(days=365),
            json.dumps(client)
        )
        
        return {
            'client_id': client_id,
            'api_key': api_key,
            'embed_code': self.generate_embed_code(client_id)
        }
    
    def get_client(self, client_id: str) -> Optional[Dict]:
        """Get client by ID"""
        data = self.redis.get(f"client:{client_id}")
        if data:
            return json.loads(data)
        return None
    
    def validate_client(self, client_id: str, api_key: str) -> bool:
        """Validate client credentials"""
        client = self.get_client(client_id)
        return client and client['api_key'] == api_key
    
    def generate_embed_code(self, client_id: str) -> str:
        """Generate JavaScript embed code"""
        return f'''
<!-- AI Chatbot Widget -->
<script>
(function() {{
    var script = document.createElement('script');
    script.src = 'http://localhost:5000/static/js/chatbot-widget.js';
    script.setAttribute('data-client-id', '{client_id}');
    script.async = true;
    document.head.appendChild(script);
}})();
</script>
'''
