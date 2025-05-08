import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import requests
import base64
from io import BytesIO
from PIL import Image

# Load environment variables
load_dotenv()

# Set API key and other constants
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get', methods=['POST'])
def get_response():
    user_msg = request.form.get('msg')
    file = request.files.get('file')

    # Prepare the payload for the API
    prompt = [user_msg]
    
    if file:
        img = Image.open(file)
        img_byte_arr = BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr = img_byte_arr.getvalue()
        encoded_img = base64.b64encode(img_byte_arr).decode('utf-8')

        # Append image to prompt
        image = {
            "inlineData": {
                "data": encoded_img,
                "mimeType": "image/png"
            }
        }
        prompt.append(image)

    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }

    # Send request to Gemini API
    response = requests.post(API_URL, json={"prompt": prompt}, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return jsonify({'text': data['response']['text']})
    else:
        return jsonify({'text': "Error generating response."})

if __name__ == '__main__':
    app.run(debug=True)
