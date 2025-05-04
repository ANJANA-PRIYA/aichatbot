import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image

# Load environment variables
from dotenv import load_dotenv
import os

load_dotenv()

# Set API key and other constants
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"

# Set Streamlit UI
st.title("Gemini Chatbot")
st.markdown("### Ask me anything!")

# Chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# Chat input
user_input = st.text_input("You:", "")

# File upload for images
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])

def generate_bot_response(user_msg, file=None):
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
        return data['response']['text']
    else:
        return "Error generating response."

# Display the chat history
for msg in st.session_state['messages']:
    if msg['role'] == "user":
        st.markdown(f"<p style='text-align:right'>{msg['text']}</p>", unsafe_allow_html=True)
    else:
        st.markdown(f"<p>{msg['text']}</p>", unsafe_allow_html=True)

# Submit button
if user_input:
    # Add user message to chat history
    st.session_state['messages'].append({'role': 'user', 'text': user_input})

    # Generate response
    bot_response = generate_bot_response(user_input, uploaded_file)

    # Add bot message to chat history
    st.session_state['messages'].append({'role': 'bot', 'text': bot_response})

    # Clear input field
    user_input = ""
