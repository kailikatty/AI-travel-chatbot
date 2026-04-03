from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import requests
import os

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

# ✅ ใส่ Unsplash Key
UNSPLASH_ACCESS_KEY = "m8COgXw9YPG1EYxgDyydkB3C19wbp4AZmuCzJtv8hg8"

# ✅ ฟังก์ชันดึงรูป
def get_image(place):
    url = "https://api.unsplash.com/search/photos"

    params = {
        "query": place + " landmark travel",
        "per_page": 1,
        "client_id": UNSPLASH_ACCESS_KEY
    }

    try:
        res = requests.get(url, params=params)
        data = res.json()

        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]["urls"]["regular"]
        else:
            return None
    except:
        return None


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
        Answer in short bullet points under 200 words.

        User: {user_message}
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        try:
            reply = response.text
        except:
            reply = response.candidates[0].content.parts[0].text

        print("FINAL REPLY:", reply)

        # ✅ ดึงชื่อสถานที่แบบ clean
        place = user_message.lower()

        for word in ["show me", "pictures of", "picture of", "images of", "image of", "photo of"]:
            place = place.replace(word, "")

        place = place.strip()

        # ✅ เรียก Unsplash
        image_url = get_image(place)

        # ✅ ปรับข้อความให้ match รูป
        if image_url:
            reply = f"Here’s what {place.title()} looks like 👇\n\n" + reply

        return jsonify({
            "reply": reply,
            "image_url": image_url
        })

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "reply": f"Error: {str(e)}"
        })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)