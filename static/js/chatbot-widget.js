// AI Chatbot Widget JavaScript
class ChatbotWidget {
    constructor(config) {
        this.clientId = config.clientId || 'default-client';
        this.apiEndpoint = config.apiEndpoint || '/api/v1/chatbot';
        this.sessionId = this.getSessionId();
        this.isOpen = false;
        this.createWidget();
        this.addStyles();
    }
    
    getSessionId() {
        let sessionId = localStorage.getItem('chatbot_session');
        if (!sessionId) {
            sessionId = 'session_' + Math.random().toString(36).substr(2, 9);
            localStorage.setItem('chatbot_session', sessionId);
        }
        return sessionId;
    }
    
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            #ai-chatbot-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 9999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            .chatbot-toggle-btn {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                color: white;
                font-size: 24px;
                cursor: pointer;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                transition: transform 0.3s;
            }
            .chatbot-toggle-btn:hover { transform: scale(1.1); }
            .chatbot-window {
                position: absolute;
                bottom: 80px;
                right: 0;
                width: 350px;
                height: 500px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            .chatbot-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 15px 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-weight: 600;
            }
            .chatbot-header button {
                background: none;
                border: none;
                color: white;
                font-size: 20px;
                cursor: pointer;
            }
            .chatbot-messages {
                flex: 1;
                overflow-y: auto;
                padding: 20px;
                background: #f8f9fa;
            }
            .message {
                margin-bottom: 12px;
                padding: 10px 15px;
                border-radius: 15px;
                max-width: 80%;
                word-wrap: break-word;
                font-size: 14px;
                line-height: 1.4;
            }
            .message-user {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                margin-left: auto;
                border-bottom-right-radius: 5px;
            }
            .message-bot {
                background: white;
                color: #333;
                border-bottom-left-radius: 5px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }
            .chatbot-input-area {
                padding: 15px;
                background: white;
                border-top: 1px solid #e0e0e0;
                display: flex;
                gap: 10px;
            }
            .chatbot-input-area input {
                flex: 1;
                padding: 10px 15px;
                border: 1px solid #e0e0e0;
                border-radius: 25px;
                outline: none;
                font-size: 14px;
            }
            .chatbot-input-area input:focus {
                border-color: #667eea;
                box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
            }
            .chatbot-input-area button {
                padding: 10px 20px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 25px;
                cursor: pointer;
                font-weight: 600;
            }
            .chatbot-input-area button:hover { transform: scale(1.05); }
        `;
        document.head.appendChild(style);
    }
    
    createWidget() {
        const container = document.createElement('div');
        container.id = 'ai-chatbot-container';
        container.innerHTML = `
            <button id="chatbot-toggle" class="chatbot-toggle-btn">💬</button>
            <div id="chatbot-window" class="chatbot-window" style="display:none;">
                <div class="chatbot-header">
                    <span>🤖 AI Assistant</span>
                    <button id="chatbot-close">✕</button>
                </div>
                <div id="chatbot-messages" class="chatbot-messages"></div>
                <div class="chatbot-input-area">
                    <input type="text" id="chatbot-input" placeholder="Type your message...">
                    <button id="chatbot-send">Send</button>
                </div>
            </div>
        `;
        document.body.appendChild(container);
        
        this.bindEvents();
        this.addMessage('bot', 'Hello! 👋 How can I help you today?');
    }
    
    bindEvents() {
        document.getElementById('chatbot-toggle').onclick = () => this.toggle();
        document.getElementById('chatbot-close').onclick = () => this.toggle();
        document.getElementById('chatbot-send').onclick = () => this.sendMessage();
        document.getElementById('chatbot-input').onkeypress = (e) => {
            if (e.key === 'Enter') this.sendMessage();
        };
    }
    
    toggle() {
        this.isOpen = !this.isOpen;
        document.getElementById('chatbot-window').style.display = this.isOpen ? 'flex' : 'none';
        if (this.isOpen) {
            document.getElementById('chatbot-input').focus();
        }
    }
    
    async sendMessage() {
        const input = document.getElementById('chatbot-input');
        const message = input.value.trim();
        if (!message) return;
        
        this.addMessage('user', message);
        input.value = '';
        
        try {
            const response = await fetch(`${this.apiEndpoint}/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    client_id: this.clientId,
                    session_id: this.sessionId,
                    message: message
                })
            });
            
            const data = await response.json();
            this.addMessage('bot', data.response || data.answer || 'I received your message!');
        } catch (error) {
            this.addMessage('bot', 'Sorry, I encountered an error. Please try again later.');
        }
    }
    
    addMessage(type, text) {
        const messages = document.getElementById('chatbot-messages');
        const div = document.createElement('div');
        div.className = `message message-${type}`;
        div.textContent = text;
        messages.appendChild(div);
        messages.scrollTop = messages.scrollHeight;
    }
}

// Auto-initialize if script tag has data-client-id
document.addEventListener('DOMContentLoaded', function() {
    const script = document.querySelector('script[data-client-id]');
    if (script && !window.chatbotInitialized) {
        window.chatbotInitialized = true;
        const clientId = script.getAttribute('data-client-id');
        new ChatbotWidget({ clientId });
    }
});
