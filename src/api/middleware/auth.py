"""JWT helpers for widget and API authentication."""
import os
from datetime import datetime, timedelta, timezone
from functools import wraps
from typing import Callable, Dict, Optional

import jwt
from flask import g, jsonify, request


ALGORITHM = "HS256"
WIDGET_TOKEN_TTL_MINUTES = int(os.getenv("WIDGET_TOKEN_TTL_MINUTES", "60"))


def _secret() -> str:
    secret = os.getenv("SECRET_KEY")
    if not secret or secret == "dev-secret-key-change-in-production":
        raise RuntimeError("SECRET_KEY must be configured for authenticated API access")
    return secret


def create_widget_token(client_id: str, domain: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": client_id,
        "domain": domain,
        "type": "widget",
        "iat": now,
        "exp": now + timedelta(minutes=WIDGET_TOKEN_TTL_MINUTES),
    }
    return jwt.encode(payload, _secret(), algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[Dict]:
    try:
        return jwt.decode(token, _secret(), algorithms=[ALGORITHM])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, RuntimeError):
        return None


def bearer_payload() -> Optional[Dict]:
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    return decode_token(header[7:].strip())


def require_widget_token(view: Callable):
    """Attach verified widget claims to flask.g."""
    @wraps(view)
    def wrapped(*args, **kwargs):
        claims = bearer_payload()
        if not claims or claims.get("type") != "widget":
            return jsonify({"error": "Valid widget authorization is required"}), 401
        g.widget_claims = claims
        return view(*args, **kwargs)

    return wrapped
