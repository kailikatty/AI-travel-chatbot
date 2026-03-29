from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

import os
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
print("API KEY:", os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def home():
    return "AI Travel Chatbot is running!"
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    prompt = f"""
    You are a local travel guide.
    Answer in short bullet points under 120 words.

    User: {user_message}
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
    )
        reply = response.text

    except Exception as e:
        print("ERROR:", e)
        reply = "Please try again in a moment."

    return jsonify({
        "reply": reply
    })

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
