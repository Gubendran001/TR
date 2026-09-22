import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from google import genai
from chatbot_config import SYSTEM_PROMPT

load_dotenv()

app = Flask(__name__)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None
MODEL = "gemini-3.1-flash-lite"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    message = (data.get("message") or "").strip()

    if not message:
        return jsonify({"reply": "Please enter a study question."}), 400

    if client is None:
        return jsonify({"reply": "Gemini API key is not configured."}), 500

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=f"{SYSTEM_PROMPT}\n\nStudent: {message}"
        )
        return jsonify({"reply": response.text})
    except Exception:
        return jsonify({"reply": "Sorry, I could not process your question right now."}), 500

if __name__ == "__main__":
    app.run()
