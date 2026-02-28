from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).lower()

    if "adhd" in question or "focus" in question:
        return jsonify({
            "answer":
            "Focus tips for Canvas:\n"
            "1) Study in 10–15 minute blocks.\n"
            "2) Close extra tabs to reduce distraction.\n"
            "3) Write one small task before starting.\n"
            "4) Use headings in Canvas to break content into chunks."
        })

    elif "quiz" in question or "extra time" in question:
        return jsonify({
            "answer":
            "Extra time requires approved reasonable adjustments.\n"
            "Contact the University of Bradford Disability Service.\n"
            "Once approved, module staff can adjust Canvas quiz settings."
        })

    elif "alternative format" in question or "audio" in question:
        return jsonify({
            "answer":
            "To access alternative formats:\n"
            "1) Look for an 'Alternative Formats' option near course files.\n"
            "2) Try browser reader mode.\n"
            "3) Contact your module leader if formats are unavailable."
        })

    elif "contact" in question or "support" in question:
        return jsonify({
            "answer":
            "University of Bradford Support:\n"
            "- Disability Service: Study adjustments.\n"
            "- IT Services: Technical Canvas issues.\n"
            "You can email or visit the official university website."
        })

    else:
        return jsonify({
            "answer":
            "I'm a prototype accessibility chatbot.\n"
            "Please ask about ADHD, focus, quiz adjustments, alternative formats, or support services."
        })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)