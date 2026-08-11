"""
Client Management API Routes
"""
from flask import Blueprint, request, jsonify
from src.clients.client_manager import ClientManager

client_bp = Blueprint('client', __name__, url_prefix='/api/v1/clients')
client_manager = ClientManager()

@client_bp.route('/register', methods=['POST'])
def register_client():
    """Register a new client"""
    try:
        data = request.get_json()
        result = client_manager.register_client(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@client_bp.route('/<client_id>', methods=['GET'])
def get_client(client_id):
    """Get client information"""
    client = client_manager.get_client(client_id)
    if client:
        # Remove sensitive data
        client.pop('api_key', None)
        client.pop('openai_api_key', None)
        return jsonify(client)
    return jsonify({'error': 'Client not found'}), 404
