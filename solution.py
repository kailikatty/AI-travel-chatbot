from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai

app = Flask(__name__)
CORS(app)

import os
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
print("CURRENT API KEY:", os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def home():
    return "AI Travel Chatbot is running!"
@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")

        print("USER:", user_message)

        prompt = f"""
        You are a local travel guide.
        Answer in short bullet points under 120 words.

        User: {user_message}
        """

        print("PROMPT:", prompt)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        print("RAW RESPONSE:", response)

        # ดึง text แบบปลอดภัย
        try:
            reply = response.text
        except:
            reply = response.candidates[0].content.parts[0].text

        print("FINAL REPLY:", reply)

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "reply": f"Error: {str(e)}"
        })

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
