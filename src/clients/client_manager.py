"""Multi-client / tenant management for the centralized chatbot platform."""
import json
import uuid
from typing import Dict, Optional
from datetime import datetime, timedelta
from urllib.parse import urlparse

import redis


def normalize_domain(value: str) -> str:
    """Return a normalized hostname for tenant-domain lookups."""
    if not value:
        return ""
    candidate = value.strip()
    if not candidate.startswith(("http://", "https://")):
        candidate = f"https://{candidate}"
    hostname = (urlparse(candidate).hostname or "").lower().strip(".")
    if hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname


class ClientManager:
    def __init__(self, redis_client: redis.Redis = None):
        self.redis = redis_client or redis.from_url(
            "redis://localhost:6379",
            decode_responses=True,
        )

    def register_client(self, client_data: Dict) -> Dict:
        """Register a customer and index its website domain."""
        required = ["name", "industry", "website_url"]
        missing = [field for field in required if not client_data.get(field)]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        client_id = str(uuid.uuid4())
        api_key = f"sk-{uuid.uuid4().hex}"
        domain = normalize_domain(client_data["website_url"])
        if not domain:
            raise ValueError("website_url must contain a valid domain")

        client = {
            "client_id": client_id,
            "name": client_data["name"],
            "industry": client_data["industry"],
            "website_url": client_data["website_url"],
            "domain": domain,
            "api_key": api_key,
            "openai_api_key": client_data.get("openai_api_key"),
            "plan": client_data.get("plan", "basic"),
            "max_tokens_per_day": client_data.get("max_tokens_per_day", 100000),
            "status": "active",
            "created_at": datetime.now().isoformat(),
        }

        ttl = timedelta(days=365)
        self.redis.setex(f"client:{client_id}", ttl, json.dumps(client))
        self.redis.setex(f"client_domain:{domain}", ttl, client_id)

        return {
            "client_id": client_id,
            "api_key": api_key,
            "embed_code": self.generate_embed_code(client_id),
        }

    def get_client(self, client_id: str) -> Optional[Dict]:
        data = self.redis.get(f"client:{client_id}")
        if not data:
            return None
        return json.loads(data)

    def get_client_by_domain(self, domain: str) -> Optional[Dict]:
        client_id = self.redis.get(f"client_domain:{normalize_domain(domain)}")
        return self.get_client(client_id) if client_id else None

    def validate_client(self, client_id: str, api_key: str) -> bool:
        client = self.get_client(client_id)
        return bool(client and client.get("api_key") == api_key and client.get("status") == "active")

    def generate_embed_code(self, client_id: str) -> str:
        """Generate the centralized production widget snippet."""
        sdk_url = "https://chatbot.midget.jsscript/dynamic-ai.js"
        return f'''<!-- Dynamic AI Chatbot -->
<script src="{sdk_url}"></script>
<script>
  DynamicAI.init({{
    customerId: "{client_id}"
  }});
</script>
'''
