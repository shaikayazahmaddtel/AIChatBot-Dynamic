"""Centralized, tenant-aware chatbot API routes."""
import uuid
from typing import Dict
from urllib.parse import urlparse

from flask import Blueprint, jsonify, request, g

from src.api.middleware.auth import create_widget_token, require_widget_token
from src.core.chatbot_engine import ChatbotEngine
from src.tenants.tenant_resolver import TenantResolver, normalize_domain

chatbot_bp = Blueprint("chatbot", __name__, url_prefix="/api/v1/chatbot")
tenant_resolver = TenantResolver()
_engine_cache: Dict[str, ChatbotEngine] = {}


def _effective_site_url(data: dict) -> str:
    origin = request.headers.get("Origin")
    if origin and origin not in {"null", ""}:
        return origin
    return data.get("website_url", "")


def _get_engine(client: dict) -> ChatbotEngine:
    client_id = client["client_id"]
    engine = _engine_cache.get(client_id)
    if engine is None:
        engine = ChatbotEngine(client_id, client)
        _engine_cache[client_id] = engine
    return engine


@chatbot_bp.route("/widget/init", methods=["POST"])
def initialize_widget():
    """Validate customer/domain pairing and issue a short-lived widget token."""
    try:
        data = request.get_json(silent=True) or {}
        client_id = data.get("customerId") or data.get("client_id")
        site_url = _effective_site_url(data)

        if not client_id or not site_url:
            return jsonify({"error": "customerId and website origin are required"}), 400

        client = tenant_resolver.client_manager.get_client(client_id)
        if not client or client.get("status") != "active":
            return jsonify({"error": "Customer not found or inactive"}), 404

        if not tenant_resolver.is_allowed_origin(client, site_url):
            return jsonify({"error": "Website domain is not registered for this customer"}), 403

        domain = normalize_domain(site_url)
        token = create_widget_token(client_id, domain)

        return jsonify({
            "status": "success",
            "customerId": client_id,
            "domain": domain,
            "token": token,
            "widgetUrl": "/widget",
        })
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 500
    except Exception:
        return jsonify({"error": "Unable to initialize chatbot widget"}), 500


@chatbot_bp.route("/init", methods=["POST"])
def initialize_chatbot():
    """Backwards-compatible initialization endpoint for server-side clients."""
    data = request.get_json(silent=True) or {}
    client_id = data.get("client_id")
    website_url = data.get("website_url")
    if not client_id or not website_url:
        return jsonify({"error": "client_id and website_url required"}), 400

    client = tenant_resolver.client_manager.get_client(client_id)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    if not tenant_resolver.is_allowed_origin(client, website_url):
        return jsonify({"error": "Website does not match registered customer domain"}), 403

    return jsonify({
        "status": "success",
        "message": f"Chatbot initialized for {website_url}",
        "client_id": client_id,
    })


@chatbot_bp.route("/chat", methods=["POST"])
@require_widget_token
def chat():
    """Process a visitor question using the tenant-specific RAG engine."""
    try:
        data = request.get_json(silent=True) or {}
        claims = g.widget_claims
        client_id = claims.get("sub")
        session_id = data.get("session_id") or str(uuid.uuid4())
        message = (data.get("message") or "").strip()

        if not message:
            return jsonify({"error": "message is required"}), 400

        client = tenant_resolver.client_manager.get_client(client_id)
        if not client or client.get("status") != "active":
            return jsonify({"error": "Customer is not available"}), 403

        token_domain = claims.get("domain", "")
        if not tenant_resolver.is_allowed_origin(client, token_domain):
            return jsonify({"error": "Customer domain validation failed"}), 403

        engine = _get_engine(client)
        result = engine.process_message(session_id=session_id, message=message)
        return jsonify(result)
    except Exception:
        return jsonify({
            "error": "Unable to process the message",
            "session_id": session_id if "session_id" in locals() else None,
        }), 500


@chatbot_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy", "version": "1.1.0"})
