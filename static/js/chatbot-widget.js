(function(){
    class ChatbotWidget{
        constructor(config){
            this.customerId=config.customerId;
            this.apiUrl=config.apiUrl;
            this.sessionId=localStorage.getItem('cs_'+this.customerId)||'s_'+Math.random().toString(36).substr(2,9);
            localStorage.setItem('cs_'+this.customerId,this.sessionId);
            this.isOpen=false;
            this.init();
        }
        init(){
            this.addStyles();
            this.createWidget();
            this.bindEvents();
            this.addMessage('bot','Hello! How can I help you? 👋');
        }
        addStyles(){
            const s=document.createElement('style');
            s.textContent='#cb-w{position:fixed;bottom:20px;right:20px;z-index:999999;font-family:-apple-system,BlinkMacSystemFont,sans-serif}.cb-btn{width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);border:none;color:white;font-size:28px;cursor:pointer;box-shadow:0 4px 20px rgba(0,0,0,.3)}.cb-win{display:none;position:absolute;bottom:80px;right:0;width:370px;height:550px;background:white;border-radius:15px;box-shadow:0 10px 50px rgba(0,0,0,.3);flex-direction:column;overflow:hidden}.cb-win.o{display:flex}.cb-h{background:linear-gradient(135deg,#667eea,#764ba2);color:white;padding:15px 20px;font-weight:bold;display:flex;justify-content:space-between}.cb-h button{background:none;border:none;color:white;font-size:22px;cursor:pointer}.cb-m{flex:1;overflow-y:auto;padding:20px;background:#f7f7f8}.cb-msg{margin-bottom:12px;padding:12px 16px;border-radius:15px;max-width:85%;word-wrap:break-word;font-size:14px;line-height:1.5}.cb-msg-u{background:#667eea;color:white;margin-left:auto;border-bottom-right-radius:5px}.cb-msg-b{background:white;color:#333;border-bottom-left-radius:5px;box-shadow:0 2px 5px rgba(0,0,0,.05)}.cb-in{padding:15px;background:white;border-top:1px solid #e5e5e5;display:flex;gap:10px}.cb-in input{flex:1;padding:12px 18px;border:2px solid #e5e5e5;border-radius:25px;outline:none;font-size:14px}.cb-in input:focus{border-color:#667eea}.cb-in button{padding:12px 24px;background:linear-gradient(135deg,#667eea,#764ba2);color:white;border:none;border-radius:25px;cursor:pointer;font-weight:600}';
            document.head.appendChild(s);
        }
        createWidget(){
            const c=document.createElement('div');c.id='cb-w';
            c.innerHTML='<button class="cb-btn" id="cb-btn">💬</button><div class="cb-win" id="cb-win"><div class="cb-h"><span>🤖 AI Assistant</span><button id="cb-close">✕</button></div><div class="cb-m" id="cb-m"></div><div class="cb-in"><input type="text" id="cb-input" placeholder="Type your message..."><button id="cb-send">Send</button></div></div>';
            document.body.appendChild(c);
        }
        bindEvents(){
            document.getElementById('cb-btn').onclick=()=>this.toggle();
            document.getElementById('cb-close').onclick=()=>this.toggle();
            document.getElementById('cb-send').onclick=()=>this.send();
            document.getElementById('cb-input').onkeypress=e=>{if(e.key==='Enter')this.send()};
        }
        toggle(){
            this.isOpen=!this.isOpen;
            document.getElementById('cb-win').classList.toggle('o');
            if(this.isOpen)document.getElementById('cb-input').focus();
        }
        async send(){
            const i=document.getElementById('cb-input'),m=i.value.trim();
            if(!m)return;
            this.addMessage('u',m);i.value='';
            try{
                const r=await fetch(this.apiUrl+'/api/v1/chatbot/'+this.customerId+'/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:this.sessionId,message:m})});
                const d=await r.json();
                this.addMessage('b',d.response||'Error');
            }catch(e){this.addMessage('b','Connection error');}
        }
        addMessage(t,text){
            const d=document.createElement('div');
            d.className='cb-msg cb-msg-'+t;
            d.textContent=text;
            document.getElementById('cb-m').appendChild(d);
            document.getElementById('cb-m').scrollTop=document.getElementById('cb-m').scrollHeight;
        }
    }
    const script=document.currentScript||document.querySelector('script[data-customer-id]');
    if(script){
        const cid=script.getAttribute('data-customer-id');
        const api=script.getAttribute('data-api-url')||window.location.origin;
        if(cid)new ChatbotWidget({customerId:cid,apiUrl:api});
    }
})();
