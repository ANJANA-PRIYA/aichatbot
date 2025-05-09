from flask import Flask, request, jsonify
from serverless_wsgi import handle_request  # Ensure this package is installed

app = Flask(__name__)

@app.route("/api/get", methods=["POST"])
def chatbot():
    user_msg = request.form.get("msg", "")
    file = request.files.get("file", None)

    # Basic response logic — replace with your chatbot logic
    if user_msg:
        reply = f"You said: {user_msg}"
    else:
        reply = "I didn't understand that."

    return jsonify({"text": reply})

# Lambda handler for Netlify
def handler(event, context):
    return handle_request(app, event, context)


