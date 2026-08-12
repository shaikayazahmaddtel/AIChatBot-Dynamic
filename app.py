"""Main application entry point for the centralized Dynamic AI Chatbot platform."""
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

load_dotenv()


def create_app(config_name=None):
    config_name = config_name or os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///chatbot.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False
    app.config["ENV"] = config_name

    # The widget is loaded by customer sites, so API requests must support cross-origin access.
    # Tenant validation is enforced by the widget-init endpoint rather than by trusting CORS.
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from src.api.routes.chatbot_routes import chatbot_bp
    from src.api.routes.client_routes import client_bp
    from src.api.routes.admin_routes import admin_bp

    app.register_blueprint(chatbot_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def index():
        return render_template("dashboard.html")

    @app.route("/api")
    def api_docs():
        return render_template("api_docs.html")

    @app.route("/api/test")
    def test_api():
        return jsonify({
            "status": "success",
            "message": "AI Chatbot API is running successfully",
            "version": "1.1.0",
            "timestamp": datetime.now().isoformat(),
            "endpoints": {
                "dashboard": "/",
                "api_docs": "/api",
                "health_check": "/api/v1/chatbot/health",
                "widget_init": "POST /api/v1/chatbot/widget/init",
                "init_chatbot": "POST /api/v1/chatbot/init",
                "send_message": "POST /api/v1/chatbot/chat",
                "register_client": "POST /api/v1/clients/register",
                "get_client": "GET /api/v1/clients/<client_id>",
                "admin_dashboard": "GET /api/v1/admin/dashboard",
                "admin_clients": "GET /api/v1/admin/clients",
            },
        })

    @app.route("/widget")
    def widget():
        """Central chatbot iframe UI loaded by the customer-site SDK."""
        return render_template("widget.html")

    @app.route("/widget-test")
    def widget_test():
        return render_template("widget_test.html")

    @app.route("/health")
    def health():
        return jsonify({
            "status": "healthy",
            "service": "AI Chatbot System",
            "version": "1.1.0",
            "timestamp": datetime.now().isoformat(),
        })

    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith("/api/"):
            return jsonify({"error": "Endpoint not found", "status": 404}), 404
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error", "status": 500}), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", 5000))
    print(f"AI Chatbot System listening on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG", "false").lower() == "true")
