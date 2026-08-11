from datetime import datetime
from src.models import db

class Client(db.Model):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.String(36), unique=True, nullable=False, index=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255))
    industry = db.Column(db.String(100))
    website_url = db.Column(db.Text)
    api_key = db.Column(db.String(128), unique=True)
    openai_api_key = db.Column(db.String(128))
    plan = db.Column(db.String(50), default='basic')
    status = db.Column(db.String(20), default='active')
    max_tokens_per_day = db.Column(db.Integer, default=100000)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
