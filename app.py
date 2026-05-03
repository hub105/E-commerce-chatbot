from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)

API_KEY = "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"
client = Groq(api_key=API_KEY)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>ShopEase Store</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f0f0; display: flex; flex-direction: column; height: 100vh; }
        .header { background: #1a0030; color: white; padding: 12px 16px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.3); }
        .header-avatar { background: #2a0050; border-radius: 50%; width: 45px; height: 45px; display: flex; align-items: center; justify-content: center; font-size: 22px; border: 2px solid #cc44ff; }
        .header-info h2 { font-size: 17px; color: #e0aaff; }
        .header-info p { font-size: 12px; opacity: 0.8; }
        .hero { background: linear-gradient(rgba(0,0,0,0.60), rgba(0,0,0,0.60)), url('https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=800') center/cover; padding: 28px 20px; color: white; text-align: center; }
        .hero h3 { font-size: 20px; margin-bottom: 6px; color: #e0aaff; }
        .hero p { font-size: 13px; opacity: 0.9; margin-bottom: 16px; }
        .hero-buttons { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
        .hero-btn { background: rgba(204,68,255,0.15); border: 2px solid #cc44ff; color: #e0aaff; padding: 8px 18px; border-radius: 20px; font-size: 13px; cursor: pointer; backdrop-filter: blur(4px); }
        .hero-btn:hover { background: #cc44ff; color: #1a0030; }
        .chat-box { flex: 1; overflow-y: auto; padding: 12px 16px; background: #f9f4ff; }
        .message { margin: 6px 0; display: flex; flex-direction: column; }
        .message.user { align-items: flex-end; }
        .message.bot { align-items: flex-start; }
        .bubble { max-width: 78%; padding: 10px 14px; border-radius: 18px; font-size: 14px; line-height: 1.6; position: relative; box-shadow: 0 1px 2px rgba(0,0,0,0.15); }
        .user .bubble { background: #1a0030; border: 1px solid #cc44ff; color: #e0aaff; border-bottom-right-radius: 4px; }
        .bot .bubble { background: #ffffff; border: 1px solid rgba(204,68,255,0.3); color: #1a0030; border-bottom-left-radius: 4px; }
        .time { font-size: 10px; color: #888; margin-top: 3px; padding: 0 4px; }
        .input-area { display: flex; padding: 10px 12px; background: #f0e6ff; gap: 8px; align-items: center; border-top: 1px solid rgba(204,68,255,0.3); }
        .input-area input { flex: 1; padding: 11px 16px; border: 1px solid rgba(204,68,255,0.4); border-radius: 24px; background: #ffffff; color: #1a0030; font-size: 14px; outline: none; }
        .input-area input::placeholder { color: #888; }
        .input-area input:focus { border-color: #cc44ff; }
        .input-area button { background: linear-gradient(135deg, #cc44ff, #8800cc); color: white; border: none; border-radius: 50%; width: 44px; height: 44px; font-size: 18px; cursor: pointer; box-shadow: 0 2px 5px rgba(204,68,255,0.4); font-weight: bold; }
        .footer { text-align: center; font-size: 11px; color: #cc44ff; padding: 6px; background: #f0e6ff; letter-spacing: 1px; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-avatar">🛍️</div>
        <div class="header-info">
            <h2>ShopEase Store</h2>
            <p>🟢 Aria AI Assistant • Available 24/7</p>
        </div>
    </div>

    <div class="hero">
        <h3>Welcome to ShopEase Store</h3>
        <p>Fashion • Electronics • Beauty • Home & Living</p>
        <div class="hero-buttons">
            <button class="hero-btn" onclick="quickSend('Show me your products')">🛒 Products</button>
            <button class="hero-btn" onclick="quickSend('How do I track my order?')">📦 Track Order</button>
            <button class="hero-btn" onclick="quickSend('What is your return policy?')">↩️ Returns</button>
            <button class="hero-btn" onclick="quickSend('Do you offer discounts?')">🏷️ Deals</button>
        </div>
    </div>

    <div class="chat-box" id="chat">
        <div class="message bot">
            <div class="bubble">Hello! I am Aria, your ShopEase AI shopping assistant powered by Atlas Automations. Whether you need help finding a product, tracking an order, or learning about our deals — I am here for you. How may I assist you today?</div>
            <div class="time">Now</div>
        </div>
    </div>

    <div class="footer">🛍️ Powered by Atlas Automations AI</div>

    <div class="input-area">
        <input type="text" id="msg" placeholder="Ask me anything about our store..." />
        <button onclick="send()">➤</button>
    </div>

    <script>
        let messages = [{role:"system", content:"You are Aria, a friendly and helpful AI shopping assistant for ShopEase Store powered by Atlas Automations. Help customers with: products (Fashion - men and women clothing, shoes and accessories, Electronics - phones, laptops, accessories, Beauty - skincare, makeup, haircare, Home and Living - furniture, kitchen, decor), pricing (items range from 5000 Naira to 500000 Naira depending on category), order tracking (customers provide order ID and you confirm it is being processed and will be delivered in 3 to 5 business days), shipping (free delivery on orders above 50000 Naira, standard delivery fee is 2500 Naira, express delivery is 5000 Naira), returns policy (items can be returned within 7 days of delivery if unused and in original packaging), payment methods (bank transfer, card payment, pay on delivery available), discounts (new customers get 10 percent off first order with code WELCOME10, seasonal sales announced on the website), customer support (support@shopeasestore.com, 08098765432, available Monday to Saturday 8am to 6pm). Always collect the customer name to personalise the experience. Use a friendly, enthusiastic and helpful tone. Keep responses 2 to 4 sentences. Always end with a warm offer to assist further."}];

        function getTime() {
            return new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }

        function addMessage(text, sender) {
            const chat = document.getElementById("chat");
            const div = document.createElement("div");
            div.className = "message " + sender;
            div.innerHTML = '<div class="bubble">' + text + '</div><div class="time">' + getTime() + '</div>';
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        async function send() {
            const input = document.getElementById("msg");
            const text = input.value.trim();
            if (!text) return;
            addMessage(text, "user");
            input.value = "";
            messages.push({role: "user", content: text});
            addMessage("typing...", "bot");
            const res = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({messages: messages})
            });
            const data = await res.json();
            const chat = document.getElementById("chat");
            chat.removeChild(chat.lastChild);
            addMessage(data.reply, "bot");
            messages.push({role: "assistant", content: data.reply});
        }

        function quickSend(text) {
            document.getElementById("msg").value = text;
            send();
        }

        document.getElementById("msg").addEventListener("keypress", function(e) {
            if (e.key === "Enter") send();
        });
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data["messages"]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
