import os
from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_cors import CORS
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from datetime import datetime, timezone
from dotenv import load_dotenv
import uuid
import json

load_dotenv()

from models import db, AdminUser, Customer, ChatbotConfig, ChatSession, Appointment
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///chatbot_platform.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    CORS(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_login_page'
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(AdminUser, int(user_id))
    
    with app.app_context():
        db.create_all()
        if not AdminUser.query.filter_by(username='admin').first():
            admin = AdminUser(username='admin', email='admin@chatbotplatform.com', is_super_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin created: admin / admin123")
    
    from api_routes import register_api_routes
    register_api_routes(app, db)
    
    # ==================== PUBLIC ROUTES ====================
    
    @app.route('/')
    def landing():
        from demo_data import INDUSTRY_DEMOS
        customers = Customer.query.filter_by(status='active').all()
        return render_template('landing.html', customers=customers, industries=INDUSTRY_DEMOS)
    
    @app.route('/demo')
    def demo_page():
        from demo_data import INDUSTRY_DEMOS
        return render_template('demo.html', industries=INDUSTRY_DEMOS)
    
    @app.route('/demo/<industry>')
    def demo_chatbot(industry):
        from demo_data import INDUSTRY_DEMOS
        if industry not in INDUSTRY_DEMOS:
            return redirect(url_for('demo_page'))
        demo_config = INDUSTRY_DEMOS[industry]
        return render_template('demo_chatbot.html', industry=industry, demo=demo_config)
    
    @app.route('/chatbot/<int:customer_id>')
    def chatbot_widget_page(customer_id):
        customer = db.session.get(Customer, customer_id)
        if not customer or customer.status != 'active':
            return "Chatbot is currently inactive", 403
        config = ChatbotConfig.query.filter_by(customer_id=customer_id).first()
        return render_template('chatbot_standalone.html', customer=customer, config=config)
    
    @app.route('/chatbot/<int:customer_id>/embed.js')
    def chatbot_embed(customer_id):
        customer = db.session.get(Customer, customer_id)
        if not customer:
            return "/* Customer not found */", 404
        base_url = request.host_url.rstrip('/')
        js_code = f"""
(function(){{var d=document,s=d.createElement('script');s.src='{base_url}/static/js/chatbot-widget.js';s.setAttribute('data-customer-id','{customer.id}');s.setAttribute('data-api-url','{base_url}');s.async=true;d.head.appendChild(s);}})();
        """
        return js_code, 200, {'Content-Type': 'application/javascript'}
    
    # ==================== ADMIN ROUTES ====================
    
    @app.route('/admin')
    def admin_login_page():
        if current_user.is_authenticated:
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_login.html')
    
    @app.route('/admin/login', methods=['POST'])
    def admin_login():
        data = request.form
        user = AdminUser.query.filter_by(username=data.get('username')).first()
        if user and user.check_password(data.get('password')):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        return render_template('admin_login.html', error='Invalid credentials')
    
    @app.route('/admin/dashboard')
    @login_required
    def admin_dashboard():
        customers = Customer.query.all()
        total_customers = len(customers)
        active_customers = sum(1 for c in customers if c.status == 'active')
        total_conversations = ChatSession.query.count()
        total_appointments = Appointment.query.count()
        monthly_revenue = sum(c.subscription_cost for c in customers if c.status == 'active')
        return render_template('admin_dashboard.html', customers=customers, total_customers=total_customers, active_customers=active_customers, total_conversations=total_conversations, total_appointments=total_appointments, monthly_revenue=monthly_revenue)
    
    @app.route('/admin/customers')
    @login_required
    def admin_customers():
        customers = Customer.query.order_by(Customer.created_at.desc()).all()
        return render_template('admin_customers.html', customers=customers)
    
    @app.route('/admin/customer/create', methods=['GET', 'POST'])
    @login_required
    def create_customer():
        if request.method == 'POST':
            data = request.form
            customer = Customer(name=data['name'], email=data.get('email'), industry=data.get('industry'), website_url=data['website_url'], subscription_cost=float(data.get('subscription_cost', 99)), status=data.get('status', 'active'), api_key=f"sk-{uuid.uuid4().hex}", created_at=datetime.now(timezone.utc))
            db.session.add(customer)
            db.session.commit()
            
            chatbot_config = ChatbotConfig(customer_id=customer.id, bot_name=f"{customer.name} Assistant", welcome_message=f"Hello! Welcome to {customer.name}. How can I help you?", theme_color=data.get('theme_color', '#667eea'), features=json.dumps({'appointment_booking': 'appointment_booking' in data, 'contact_sharing': 'contact_sharing' in data, 'live_chat': 'live_chat' in data, 'multilingual': 'multilingual' in data}))
            db.session.add(chatbot_config)
            db.session.commit()
            
            return redirect(url_for('admin_customers'))
        return render_template('create_customer.html')
    
    @app.route('/admin/customer/<int:customer_id>')
    @login_required
    def customer_detail(customer_id):
        customer = db.session.get(Customer, customer_id)
        if not customer: return "Customer not found", 404
        config = ChatbotConfig.query.filter_by(customer_id=customer_id).first()
        return render_template('customer_detail.html', customer=customer, config=config)
    
    @app.route('/admin/customer/<int:customer_id>/toggle', methods=['POST'])
    @login_required
    def toggle_customer(customer_id):
        customer = db.session.get(Customer, customer_id)
        if customer:
            customer.status = 'inactive' if customer.status == 'active' else 'active'
            db.session.commit()
        return redirect(url_for('admin_customers'))
    
    @app.route('/admin/logout')
    @login_required
    def admin_logout():
        logout_user()
        return redirect(url_for('admin_login_page'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║     🤖 Multi-Tenant AI Chatbot Platform                    ║
╠══════════════════════════════════════════════════════════════╣
║  🏠 Home:   http://localhost:{port}                           ║
║  🎮 Demo:   http://localhost:{port}/demo                      ║
║  👨‍💼 Admin:  http://localhost:{port}/admin                     ║
║  📧 Login:  admin / admin123                                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host='0.0.0.0', port=port, debug=True)
