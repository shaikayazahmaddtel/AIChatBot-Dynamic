import json
import random
import re

class DemoChatEngine:
    def __init__(self, demo_data):
        self.demo_data = demo_data
        self.name = demo_data['name']
        self.knowledge = demo_data.get('knowledge_base', {})
        self.config = demo_data.get('config', {})
        self.conversation_history = []
        self.industry = self._detect_industry()
    
    def _detect_industry(self):
        name_lower = self.name.lower()
        kb_keys = list(self.knowledge.keys())
        if any(w in name_lower for w in ['hospital', 'medical', 'clinic', 'health']):
            return 'hospital'
        elif any(w in name_lower for w in ['property', 'real', 'home', 'dream']):
            return 'real_estate'
        elif any(w in name_lower for w in ['university', 'college', 'education', 'techvision']):
            return 'education'
        elif any(w in name_lower for w in ['shop', 'mart', 'store', 'retail']):
            return 'ecommerce'
        elif any(w in name_lower for w in ['tech', 'solution', 'corp']):
            return 'corporate'
        return 'general'
    
    def generate_response(self, message):
        message_lower = message.lower().strip()
        message_words = message_lower.split()
        self.conversation_history.append({'role': 'user', 'content': message})
        
        # Very short messages - greetings
        if len(message_words) <= 2:
            if message_lower in ['hi', 'hello', 'hey', 'hola']:
                return self._get_greeting()
            if message_lower in ['yes', 'yeah', 'yep', 'sure']:
                return self._get_more_details()
            if message_lower in ['no', 'nope', 'nah']:
                return "No problem! What else can I help you with?"
        
        # Search knowledge base first
        kb_response = self._search_knowledge_base(message)
        if kb_response:
            return kb_response
        
        # Intent matching
        intent = self._detect_intent(message_lower)
        
        if intent == 'greeting' and len(message_words) <= 3:
            return self._get_greeting()
        elif intent == 'contact':
            return self._get_contact()
        elif intent == 'appointment':
            return self._get_appointment()
        elif intent == 'deals':
            return self._get_deals()
        elif intent == 'order':
            return self._get_order_info()
        elif intent == 'payment':
            return self._get_payment()
        elif intent == 'about':
            return self._get_about()
        elif intent == 'services':
            return self._get_services()
        elif intent == 'pricing':
            return self._get_pricing()
        elif intent == 'staff':
            return self._get_staff()
        elif intent == 'location':
            return self._get_location()
        elif intent == 'hours':
            return self._get_hours()
        elif intent == 'faq':
            return self._get_faq()
        elif intent == 'more_details':
            return self._get_more_details()
        
        # Fallback
        return self._get_smart_fallback(message)
    
    def _detect_intent(self, msg):
        if any(w in msg for w in ['contact', 'phone', 'number', 'call', 'email', 'address', 'reach']):
            return 'contact'
        if any(w in msg for w in ['appointment', 'book', 'schedule', 'visit', 'tour']):
            return 'appointment'
        if any(w in msg for w in ['deal', 'offer', 'discount', 'sale', 'promotion', 'coupon', 'today']):
            return 'deals'
        if any(w in msg for w in ['order', 'track', 'delivery', 'ship', 'return', 'refund', 'cancel']):
            return 'order'
        if any(w in msg for w in ['payment', 'pay', 'card', 'upi', 'emi', 'cod', 'wallet']):
            return 'payment'
        if any(w in msg for w in ['about', 'company', 'who are', 'explain', 'tell me about', 'describe']):
            return 'about'
        if any(w in msg for w in ['service', 'product', 'offer', 'provide', 'sell', 'course', 'program', 'category']):
            return 'services'
        if any(w in msg for w in ['price', 'cost', 'fee', 'charge', 'pricing', 'rate', 'amount', 'scholarship']):
            return 'pricing'
        if any(w in msg for w in ['staff', 'doctor', 'faculty', 'teacher', 'professor', 'team', 'employee', 'who works', 'how many']):
            return 'staff'
        if any(w in msg for w in ['location', 'where', 'address', 'facility', 'campus', 'office', 'branch', 'store']):
            return 'location'
        if any(w in msg for w in ['hour', 'time', 'open', 'close', 'timing', 'when']):
            return 'hours'
        if any(w in msg for w in ['help', 'faq', 'question', 'how do', 'how can', 'how to']):
            return 'faq'
        if any(w in msg for w in ['more detail', 'tell me more', 'elaborate', 'even more', 'more info']):
            return 'more_details'
        if msg in ['hi', 'hello', 'hey', 'good morning', 'good afternoon']:
            return 'greeting'
        return None
    
    def _search_knowledge_base(self, query):
        query_lower = query.lower()
        query_words = [w for w in query_lower.split() if len(w) > 2]
        if not query_words:
            return None
        
        best_score = 0
        best_sentences = []
        
        for key, content in self.knowledge.items():
            if not isinstance(content, str):
                continue
            content_lower = content.lower()
            score = sum(content_lower.count(w) for w in query_words)
            
            if score > best_score:
                best_score = score
                sentences = re.split(r'[.!?]+', content)
                best_sentences = [s.strip() for s in sentences if s.strip() and any(w in s.lower() for w in query_words)]
                if not best_sentences:
                    best_sentences = [s.strip() for s in sentences[:3] if s.strip()]
        
        if best_score >= 2 and best_sentences:
            answer = '. '.join(best_sentences[:4]) + '.'
            return f"{answer}\n\n💡 Is there anything else you'd like to know?"
        
        return None
    
    def _get_greeting(self):
        if self.industry == 'ecommerce':
            return f"👋 Welcome to {self.name}!\n\nI can help you with:\n🛍️ Today's Deals\n📦 Order Tracking\n💳 Payment Methods\n🔄 Returns & Refunds\n📞 Customer Support\n\nWhat would you like to know?"
        elif self.industry == 'hospital':
            return f"👋 Welcome to {self.name}!\n\nI can help you with:\n🏥 Our Services\n👨‍⚕️ Doctor Information\n📅 Book Appointments\n📞 Contact Details\n🕐 Visiting Hours\n\nHow can I assist you?"
        elif self.industry == 'education':
            return f"👋 Welcome to {self.name}!\n\nI can help you with:\n📚 Available Courses\n📝 Admission Process\n💰 Fee Structure\n👨‍🏫 Faculty Information\n🏫 Campus Facilities\n\nWhat would you like to know?"
        elif self.industry == 'real_estate':
            return f"👋 Welcome to {self.name}!\n\nI can help you with:\n🏠 Available Properties\n📅 Book Site Visit\n💰 Price & EMI Options\n📍 Project Locations\n📞 Contact Sales Team\n\nHow can I assist you?"
        else:
            return f"Hello! Welcome to {self.name}. How can I help you today?"
    
    def _get_contact(self):
        contact = self.config
        response = f"📞 **Contact {self.name}:**\n\n"
        if contact.get('contact_phone'): response += f"📱 Phone: {contact['contact_phone']}\n"
        if contact.get('contact_email'): response += f"📧 Email: {contact['contact_email']}\n"
        if contact.get('contact_address'): response += f"📍 Address: {contact['contact_address']}\n"
        
        # Also try knowledge base
        for key in ['contact', 'contact-us']:
            if key in self.knowledge:
                try:
                    data = json.loads(self.knowledge[key])
                    if 'phone' in data:
                        phones = data['phone'] if isinstance(data['phone'], list) else [data['phone']]
                        if not contact.get('contact_phone'):
                            response += f"📱 Phone: {', '.join(phones[:2])}\n"
                    if 'email' in data:
                        emails = data['email'] if isinstance(data['email'], list) else [data['email']]
                        if not contact.get('contact_email'):
                            response += f"📧 Email: {', '.join(emails[:2])}\n"
                    if 'address' in data and not contact.get('contact_address'):
                        response += f"📍 Address: {data['address']}\n"
                except:
                    pass
        
        return response + "\n💡 How else can I help you?"
    
    def _get_appointment(self):
        return f"📅 I'd be happy to help you schedule a visit to {self.name}!\n\nPlease provide:\n• Your full name\n• Preferred date and time\n• Purpose of visit\n• Contact number\n\nWe'll confirm your booking via SMS/Email. Would you like to proceed?"
    
    def _get_deals(self):
        if self.industry == 'ecommerce':
            return f"🛍️ **Today's Hot Deals at {self.name}:**\n\n🔥 Up to 70% off on Electronics\n🔥 Buy 1 Get 1 on Fashion\n🔥 Flat 50% off on Home Appliances\n🔥 Free Delivery on orders above ₹499\n\n💳 10% instant discount with HDFC cards\n💳 No Cost EMI on orders above ₹5000\n\n🕐 Limited Time - Grab Before They're Gone!\n\nWould you like to browse a specific category?"
        faq = self.knowledge.get('faq', '')
        return f"🎉 Here are our current offers:\n\n{faq[:300] if faq else 'Check our website for the latest deals!'}\n\nWant to know more?"
    
    def _get_order_info(self):
        faq = self.knowledge.get('faq', '')
        if self.industry == 'ecommerce':
            return f"📦 **Order Information:**\n\nTrack Order: Visit 'My Orders' on our website\nDelivery: 2-7 business days\nReturns: 30-day easy return policy\nRefunds: Within 7 business days\n\n{faq[:200] if faq else ''}\n\n📞 Need help? Contact our support team!"
        return f"📋 Here's information about orders:\n\n{faq[:400] if faq else 'Contact us for order-related queries.'}\n\nHow can I assist further?"
    
    def _get_payment(self):
        faq = self.knowledge.get('faq', '')
        for key, content in self.knowledge.items():
            if isinstance(content, str) and any(w in content.lower() for w in ['payment', 'pay', 'card', 'upi', 'cod']):
                sentences = re.split(r'[.!?]+', content)
                pay_sentences = [s.strip() for s in sentences if any(w in s.lower() for w in ['payment', 'pay', 'card', 'upi', 'cod', 'emi'])][:4]
                if pay_sentences:
                    return f"💳 **Payment Methods:**\n\n{'. '.join(pay_sentences)}.\n\nNeed help with payment?"
        return f"💳 We accept: Credit/Debit Cards, UPI, Net Banking, COD, EMI.\n\n{faq[:200] if faq else ''}\n\nWhich method would you like to know about?"
    
    def _get_about(self):
        about = self.knowledge.get('about', '') or self.knowledge.get('home', '')
        if about:
            return f"ℹ️ **About {self.name}:**\n\n{about[:600]}\n\nIs there anything specific you'd like to know?"
        return f"{self.name} is a leading provider in our industry. What would you like to know specifically?"
    
    def _get_services(self):
        services = self.knowledge.get('services', '')
        if services:
            return f"📋 **What We Offer:**\n\n{services[:600]}\n\nWould you like details about any specific item?"
        return f"We offer a wide range of products and services. What are you looking for?"
    
    def _get_pricing(self):
        faq = self.knowledge.get('faq', '')
        if faq:
            sentences = re.split(r'[.!?]+', faq)
            price_sentences = [s.strip() for s in sentences if any(w in s.lower() for w in ['price', 'cost', 'fee', '₹', '$', 'emi', 'lakh', 'crore', 'scholarship'])][:4]
            if price_sentences:
                return f"💰 **Pricing Information:**\n\n{'. '.join(price_sentences)}.\n\nWant more specific details?"
        return f"For detailed pricing, check our website or contact our team. Is there a specific product/service you'd like pricing for?"
    
    def _get_staff(self):
        doctors_data = self.knowledge.get('doctors', '')
        about = self.knowledge.get('about', '')
        response = f"👨‍💼 **Our Team at {self.name}:**\n\n"
        
        if doctors_data:
            try:
                data = json.loads(doctors_data) if isinstance(doctors_data, str) else doctors_data
                doctors = data.get('doctors', [])
                if doctors:
                    for doc in doctors[:6]:
                        response += f"• **{doc['name']}**"
                        if doc.get('specialty'): response += f" - {doc['specialty']}"
                        response += "\n"
                if about:
                    numbers = re.findall(r'(\d+[\+,]?\d*\s*(?:faculty|teacher|professor|staff|doctor|employee))', about, re.IGNORECASE)
                    if numbers: response += f"\n📊 {numbers[0]}"
                return response
            except:
                pass
        
        if about:
            return f"👨‍💼 **Our Team:**\n\n{about[:400]}\n\nWould you like to know about any specific team member?"
        return f"We have a dedicated team of professionals. What specific information are you looking for?"
    
    def _get_location(self):
        contact = self.config
        if contact.get('contact_address'):
            return f"📍 **Location:**\n\n{contact['contact_address']}\n\nWould you like directions?"
        about = self.knowledge.get('about', '')
        home = self.knowledge.get('home', '')
        all_content = about + ' ' + home
        match = re.search(r'(?:located at|situated at|address is|campus at|office at)\s*(.+?)(?:\.|$)', all_content, re.IGNORECASE)
        if match:
            return f"📍 **Location:**\n\n{match.group(1).strip()}\n\nHow can I help with directions?"
        return f"We have convenient locations. Please contact us for specific location details."
    
    def _get_hours(self):
        faq = self.knowledge.get('faq', '')
        if faq:
            hours = re.findall(r'([^.]*(?:hour|open|close|timing|schedule|am|pm)[^.]*\.)', faq, re.IGNORECASE)
            if hours:
                return f"🕐 **Business Hours:**\n\n{hours[0].strip()}\n\nNeed to schedule a visit?"
        return f"🕐 Our business hours are designed for your convenience. Check our website or contact us for specific timings."
    
    def _get_faq(self):
        faq = self.knowledge.get('faq', '')
        if faq:
            return f"❓ **Frequently Asked Questions:**\n\n{faq[:600]}\n\nDid this answer your question?"
        return f"I'm here to answer your questions! What would you like to know about {self.name}?"
    
    def _get_more_details(self):
        all_content = []
        for key, value in self.knowledge.items():
            if isinstance(value, str) and key not in ['home', 'about']:
                all_content.append(value)
        if all_content:
            for content in all_content:
                if len(content) > 100:
                    return f"📚 **More Information:**\n\n{content[:600]}\n\nWould you like even more details?"
        return self._get_about()
    
    def _get_smart_fallback(self, message):
        words = [w for w in message.lower().split() if len(w) > 3]
        all_content = ' '.join([v for v in self.knowledge.values() if isinstance(v, str)])
        
        for word in words:
            if word in all_content.lower():
                idx = all_content.lower().find(word)
                start = max(0, idx - 100)
                end = min(len(all_content), idx + 300)
                return f"I found this related to your query:\n\n{all_content[start:end]}...\n\nIs this what you were looking for?"
        
        if self.industry == 'ecommerce':
            return f"I'm here to help with shopping! Ask me about deals, orders, payments, returns, or contact support. What interests you?"
        elif self.industry == 'hospital':
            return f"I can help with medical services, doctors, appointments, and contact info. What would you like to know?"
        elif self.industry == 'education':
            return f"I can help with courses, admissions, fees, faculty, and campus info. What are you interested in?"
        elif self.industry == 'real_estate':
            return f"I can help with properties, site visits, pricing, and locations. What are you looking for?"
        else:
            return f"I'm here to help! Ask me about our services, pricing, contact info, or anything about {self.name}."
