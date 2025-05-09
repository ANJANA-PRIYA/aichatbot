from flask import Flask, request, jsonify
from serverless import handler

# Create the Flask app
app = Flask(__name__)

@app.route("/get", methods=["POST"])
def get_response():
    # Retrieve message from the request
    user_message = request.form.get("msg")
    file = request.files.get("file")

    # Logic to handle the user message and file (you can expand this)
    # For now, just return a static bot message
    response_message = f"Bot received: {user_message}"

    # You can add file handling logic here if necessary

    return jsonify({"text": response_message})

# Adapt the Flask app to be a serverless function
def lambda_handler(event, context):
    return handler(app, event, context)



