import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# Read your Groq key from environment variable
# On Render you'll set GROQ_API_KEY in Environment settings
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"  # you can change later

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()

    if not question:
        return jsonify({"answer": "Please type a question."})

    system_msg = (
        "You are a University of Bradford Canvas accessibility support chatbot. "
        "Give calm, short, step-by-step guidance for neurodiverse students. "
        "Do not claim you can access a student's Canvas data. "
        "If unsure, say so and suggest contacting University support services."
    )

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": question},
            ],
            temperature=0.4,
            max_tokens=350,
        )
        answer = resp.choices[0].message.content.strip()
        return jsonify({"answer": answer})
    except Exception as e:
        return jsonify({"answer": f"Server error: {e}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
