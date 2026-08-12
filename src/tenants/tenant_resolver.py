"""Tenant and domain resolution for the centralized chatbot platform."""
from urllib.parse import urlparse
from typing import Dict, Optional

from src.clients.client_manager import ClientManager


def normalize_domain(value: str) -> str:
    """Normalize a URL/host into a comparable hostname."""
    if not value:
        return ""
    candidate = value.strip()
    if not candidate.startswith(("http://", "https://")):
        candidate = f"https://{candidate}"
    hostname = (urlparse(candidate).hostname or "").lower().strip(".")
    if hostname.startswith("www."):
        hostname = hostname[4:]
    return hostname


class TenantResolver:
    """Resolve a registered customer from an allowed website domain."""

    def __init__(self, client_manager: Optional[ClientManager] = None):
        self.client_manager = client_manager or ClientManager()

    def resolve_by_domain(self, origin_or_url: str) -> Optional[Dict]:
        domain = normalize_domain(origin_or_url)
        if not domain:
            return None
        return self.client_manager.get_client_by_domain(domain)

    def is_allowed_origin(self, client: Dict, origin_or_url: str) -> bool:
        """Check that a request originated from the tenant's registered domain."""
        if not client:
            return False
        requested_domain = normalize_domain(origin_or_url)
        registered_domain = normalize_domain(client.get("website_url", ""))
        return bool(requested_domain and registered_domain and requested_domain == registered_domain)
