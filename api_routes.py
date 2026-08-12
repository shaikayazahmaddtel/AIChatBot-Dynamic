from flask import request, jsonify
from datetime import datetime, timezone
import uuid
import json
from models import Customer, ChatbotConfig, ChatSession, ChatMessage, Appointment
from demo_chat_engine import DemoChatEngine
from demo_data import INDUSTRY_DEMOS

def register_api_routes(app, db):
    
    @app.route('/api/v1/demo/chat', methods=['POST'])
    def demo_chat():
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data provided'}), 400
            
            industry = data.get('industry', 'hospital')
            message = data.get('message', '')
            session_id = data.get('session_id', str(uuid.uuid4()))
            
            if not message:
                return jsonify({'error': 'Message is required'}), 400
            
            if industry not in INDUSTRY_DEMOS:
                return jsonify({'error': 'Invalid industry', 'valid': list(INDUSTRY_DEMOS.keys())}), 400
            
            demo_data = INDUSTRY_DEMOS[industry]
            engine = DemoChatEngine(demo_data)
            response = engine.generate_response(message)
            
            return jsonify({
                'session_id': session_id,
                'response': response,
                'demo_name': demo_data['name'],
                'industry': industry
            })
        except Exception as e:
            print(f"Demo chat error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/v1/demo/industries', methods=['GET'])
    def get_demo_industries():
        industries = []
        for key, data in INDUSTRY_DEMOS.items():
            industries.append({
                'id': key,
                'name': data['name'],
                'icon': data['icon'],
                'description': data['description'],
                'sample_questions': data['sample_questions']
            })
        return jsonify({'industries': industries})
    
    @app.route('/api/v1/chatbot/<int:customer_id>/chat', methods=['POST'])
    def chatbot_chat(customer_id):
        try:
            data = request.get_json()
            message = data.get('message')
            session_id = data.get('session_id')
            
            if not message:
                return jsonify({'error': 'Message is required'}), 400
            
            customer = db.session.get(Customer, customer_id)
            if not customer:
                return jsonify({'error': 'Customer not found'}), 404
            
            if session_id:
                chat_session = ChatSession.query.filter_by(session_id=session_id).first()
            
            if not session_id or not chat_session:
                session_id = str(uuid.uuid4())
                chat_session = ChatSession(session_id=session_id, customer_id=customer_id, visitor_ip=request.remote_addr)
                db.session.add(chat_session)
                db.session.commit()
            
            user_msg = ChatMessage(session_id=chat_session.id, role='user', content=message)
            db.session.add(user_msg)
            
            response = _generate_customer_response(customer, message)
            
            bot_msg = ChatMessage(session_id=chat_session.id, role='assistant', content=response)
            db.session.add(bot_msg)
            
            chat_session.message_count += 2
            chat_session.last_message_at = datetime.now(timezone.utc)
            customer.total_conversations += 1
            db.session.commit()
            
            return jsonify({'session_id': session_id, 'response': response, 'customer_name': customer.name})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    @app.route('/api/v1/chatbot/<int:customer_id>/appointment', methods=['POST'])
    def book_appointment(customer_id):
        try:
            data = request.get_json()
            customer = db.session.get(Customer, customer_id)
            if not customer:
                return jsonify({'error': 'Customer not found'}), 404
            
            appointment = Appointment(
                customer_id=customer_id,
                patient_name=data.get('name'),
                patient_email=data.get('email'),
                patient_phone=data.get('phone'),
                department=data.get('department'),
                doctor_name=data.get('doctor'),
                reason=data.get('reason'),
                status='confirmed'
            )
            db.session.add(appointment)
            customer.total_appointments += 1
            db.session.commit()
            
            return jsonify({'status': 'success', 'message': 'Appointment booked!', 'appointment_id': appointment.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

def _generate_customer_response(customer, message):
    try:
        knowledge = json.loads(customer.knowledge_base) if customer.knowledge_base else {}
        msg_lower = message.lower()
        
        if any(w in msg_lower for w in ['appointment', 'book', 'schedule']):
            return f"I'd be happy to help you book at {customer.name}! Please provide your name, preferred date/time, and contact number."
        if any(w in msg_lower for w in ['contact', 'phone', 'email', 'address']):
            config = ChatbotConfig.query.filter_by(customer_id=customer.id).first()
            resp = f"📞 Contact {customer.name}:\n"
            if config:
                if config.contact_phone: resp += f"📱 {config.contact_phone}\n"
                if config.contact_email: resp += f"📧 {config.contact_email}\n"
                if config.contact_address: resp += f"📍 {config.contact_address}\n"
            return resp + f"\n🌐 {customer.website_url}"
        
        # Search knowledge base
        for key, content in knowledge.items():
            if isinstance(content, str) and any(w in content.lower() for w in msg_lower.split()):
                return f"{content[:500]}\n\nIs there anything else you'd like to know?"
        
        return f"Thank you for your interest in {customer.name}! How can I help you? Visit {customer.website_url} for more information."
    except:
        return f"Welcome to {customer.name}! How can I assist you today?"
