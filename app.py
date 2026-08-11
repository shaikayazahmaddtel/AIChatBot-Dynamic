"""
Main Application Entry Point
Dynamic AI Chatbot System for Multiple Clients
"""
import os
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    
    # Basic configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///chatbot.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_SORT_KEYS'] = False
    
    # Enable CORS
    CORS(app)
    
    # Import and register blueprints
    try:
        from src.api.routes.chatbot_routes import chatbot_bp
        from src.api.routes.client_routes import client_bp
        from src.api.routes.admin_routes import admin_bp
        
        app.register_blueprint(chatbot_bp)
        app.register_blueprint(client_bp)
        app.register_blueprint(admin_bp)
    except ImportError as e:
        print(f"Warning: Could not import blueprints: {e}")
    
    # ============= ROUTES =============
    
    @app.route('/')
    def index():
        """Main dashboard page"""
        return render_template('dashboard.html')
    
    @app.route('/api')
    def api_docs():
        """API documentation page"""
        return render_template('api_docs.html')
    
    @app.route('/api/test')
    def test_api():
        """Test endpoint to verify API is working"""
        return jsonify({
            'status': 'success',
            'message': '🎉 AI Chatbot API is running successfully!',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat(),
            'endpoints': {
                'dashboard': '/',
                'api_docs': '/api',
                'health_check': '/api/v1/chatbot/health',
                'test_api': '/api/test',
                'init_chatbot': 'POST /api/v1/chatbot/init',
                'send_message': 'POST /api/v1/chatbot/chat',
                'register_client': 'POST /api/v1/clients/register',
                'get_client': 'GET /api/v1/clients/<client_id>',
                'admin_dashboard': 'GET /api/v1/admin/dashboard',
                'admin_clients': 'GET /api/v1/admin/clients'
            }
        })
    
    @app.route('/widget-test')
    def widget_test():
        """Test page for chatbot widget"""
        return render_template('widget_test.html')
    
    @app.route('/health')
    def health():
        """Simple health check"""
        return jsonify({
            'status': 'healthy',
            'service': 'AI Chatbot System',
            'version': '1.0.0',
            'timestamp': datetime.now().isoformat()
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Endpoint not found', 'status': 404}), 404
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        return jsonify({'error': 'Internal server error', 'status': 500}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    print(f"""
╔══════════════════════════════════════════════════════════╗
║          🤖 AI Chatbot System is Starting...            ║
╠══════════════════════════════════════════════════════════╣
║  📍 Dashboard:  http://localhost:{port}                   ║
║  📚 API Docs:   http://localhost:{port}/api               ║
║  🧪 API Test:   http://localhost:{port}/api/test          ║
║  💬 Widget:     http://localhost:{port}/widget-test       ║
║  ❤️  Health:     http://localhost:{port}/health            ║
╚══════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port, debug=True)
