from flask import Flask, request, jsonify, render_template_string
import requests

app = Flask(__name__)

# ========================
# 🔑 Your OpenRouter API key
# ========================
OPENROUTER_API_KEY = "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"  # <- replace with your full key
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# ========================
# Frontend HTML/CSS/JS
# ========================
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Daffodils Ai (Class 10)</title>
<style>
body { margin:0; background:#0f172a; color:white; font-family:Poppins,sans-serif; display:flex; justify-content:center; align-items:center; height:100vh; }
.chat-container { background: rgba(255,255,255,0.05); width:420px; height:600px; border-radius:20px; padding:20px; display:flex; flex-direction:column; box-shadow:0 0 25px rgba(0,255,255,0.2); }
h1 { text-align:center; margin-bottom:15px; color:#38bdf8; }
.chat-box { flex:1; overflow-y:auto; border-radius:10px; background: rgba(0,0,0,0.2); padding:10px; }
.message { margin:8px 0; line-height:1.4em; padding:10px; border-radius:10px; max-width:85%; }
.user { background:#2563eb; align-self:flex-end; }
.bot { background:#334155; align-self:flex-start; }
.input-area { display:flex; gap:8px; margin-top:10px; }
input { flex:1; padding:10px; border-radius:10px; border:none; outline:none; font-size:16px; }
button { background:#38bdf8; color:white; border:none; padding:10px 20px; border-radius:10px; cursor:pointer; transition:0.3s; }
button:hover { background:#0ea5e9; }
</style>
</head>
<body>
<div class="chat-container">
  <h1>💬 Daffodils Ai Class 10</h1>
  <div id="chatBox" class="chat-box"></div>
  <div class="input-area">
    <input id="userInput" type="text" placeholder="Type your message..." />
    <button id="sendBtn">Send</button>
  </div>
</div>
<script>
const sendBtn = document.getElementById("sendBtn");
const userInput = document.getElementById("userInput");
const chatBox = document.getElementById("chatBox");

sendBtn.onclick = async () => {
  const message = userInput.value.trim();
  if(!message) return;

  addMessage("user", message);
  userInput.value = "";
  addMessage("bot", "Thinking...");

  try {
    const res = await fetch("/chat", {
      method:"POST",
      headers: {"Content-Type":"application/json"},
      body: JSON.stringify({message})
    });
    const data = await res.json();
    document.querySelector(".bot:last-child").textContent = data.reply;
  } catch(err){
    document.querySelector(".bot:last-child").textContent = "❌ Error connecting to server.";
  }
};

function addMessage(role, text){
  const div = document.createElement("div");
  div.classList.add("message", role);
  div.textContent = text;
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}
</script>
</body>
</html>
"""

# ========================
# Serve frontend
# ========================
@app.route("/")
def home():
    return render_template_string(HTML_PAGE)

# ========================
# Chat endpoint
# ========================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"reply":"Please type something first!"})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "http://localhost:5000",
        "X-Title": "Aashish Chat",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages":[
            {"role":"system","content":"You are Daffodils Ai, a smart and friendly AI assistant."},
            {"role":"user","content": user_message}
        ]
    }

    try:
        response = requests.post(OPENROUTER_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        print("Error:", e)
        reply = "❌ Something went wrong. Check your API key or internet."

    return jsonify({"reply": reply})

# ========================
# Run server
# ========================
if __name__ == "__main__":
    app.run(debug=True)
