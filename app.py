import os
from flask import Flask, render_template, request, jsonify, session
from groq import Groq

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "change-this-secret-key")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"

SYSTEM_MSG = (
    "You are a University of Bradford Canvas accessibility support chatbot. "
    "Give calm, short, step-by-step guidance for neurodiverse students. "
    "Use simple language. "
    "Do not claim you can access a student's Canvas data. "
    "If unsure, say so and suggest contacting University support services."
)

MAX_HISTORY = 10

@app.get("/")
def home():
    return render_template("chatbot.html")  # change this if your html file has another name

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()

    if not question:
        return jsonify({"answer": "Please type a question."}), 400

    history = session.get("history", [])

    messages = [{"role": "system", "content": SYSTEM_MSG}]
    messages.extend(history)
    messages.append({"role": "user", "content": question})

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.4,
            max_tokens=350,
        )

        answer = resp.choices[0].message.content.strip()

        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
        session["history"] = history[-MAX_HISTORY:]

        return jsonify({"answer": answer})

    except Exception:
        return jsonify({
            "answer": "Sorry, something went wrong on the server. Please try again."
        }), 500

@app.post("/api/clear")
def clear_chat():
    session.pop("history", None)
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
