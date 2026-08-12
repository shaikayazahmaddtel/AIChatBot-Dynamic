from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class AdminUser(UserMixin, db.Model):
    __tablename__ = 'admin_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    is_super_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Customer(db.Model):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    industry = db.Column(db.String(100))
    website_url = db.Column(db.String(500))
    subscription_cost = db.Column(db.Float, default=0.0)
    status = db.Column(db.String(20), default='active')
    api_key = db.Column(db.String(128), unique=True)
    knowledge_base = db.Column(db.Text)
    last_crawled = db.Column(db.DateTime)
    total_conversations = db.Column(db.Integer, default=0)
    total_appointments = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    chatbot_config = db.relationship('ChatbotConfig', backref='customer', uselist=False)
    sessions = db.relationship('ChatSession', backref='customer', lazy='dynamic')

class ChatbotConfig(db.Model):
    __tablename__ = 'chatbot_configs'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), unique=True)
    bot_name = db.Column(db.String(255))
    welcome_message = db.Column(db.Text)
    theme_color = db.Column(db.String(7), default='#667eea')
    position = db.Column(db.String(20), default='bottom-right')
    features = db.Column(db.Text)
    ai_provider = db.Column(db.String(50), default='openai')
    ai_model = db.Column(db.String(100), default='gpt-3.5-turbo')
    ai_temperature = db.Column(db.Float, default=0.7)
    ai_max_tokens = db.Column(db.Integer, default=2000)
    business_hours = db.Column(db.Text)
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(50))
    contact_address = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def get_features(self):
        return json.loads(self.features) if self.features else {}

class ChatSession(db.Model):
    __tablename__ = 'chat_sessions'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), unique=True, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    visitor_ip = db.Column(db.String(45))
    message_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_message_at = db.Column(db.DateTime)
    messages = db.relationship('ChatMessage', backref='session', lazy='dynamic')

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('chat_sessions.id'))
    role = db.Column(db.String(20))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Appointment(db.Model):
    __tablename__ = 'appointments'
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    patient_name = db.Column(db.String(255))
    patient_email = db.Column(db.String(255))
    patient_phone = db.Column(db.String(50))
    appointment_date = db.Column(db.DateTime)
    department = db.Column(db.String(255))
    doctor_name = db.Column(db.String(255))
    reason = db.Column(db.Text)
    status = db.Column(db.String(50), default='confirmed')
    confirmation_sent = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
