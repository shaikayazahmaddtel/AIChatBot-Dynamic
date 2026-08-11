"""
Admin API Routes
"""
from flask import Blueprint, request, jsonify
from src.clients.client_manager import ClientManager

admin_bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')
client_manager = ClientManager()

@admin_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """Admin dashboard data"""
    return jsonify({
        'total_clients': 0,
        'active_chats': 0,
        'total_messages': 0,
        'system_health': 'healthy'
    })

@admin_bp.route('/clients', methods=['GET'])
def list_clients():
    """List all clients"""
    # Simplified - would query database
    return jsonify({'clients': [], 'total': 0})
