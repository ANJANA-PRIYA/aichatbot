from flask import Flask, request, jsonify
from serverless_wsgi import handle_request

app = Flask(__name__)

@app.route("/api/get", methods=["POST"])
def chatbot():
    user_msg = request.form.get("msg", "")
    file = request.files.get("file", None)

    if user_msg:
        reply = f"You said: {user_msg}"
    else:
        reply = "I didn't understand that."

    return jsonify({"text": reply})

def handler(event, context):
    return handle_request(app, event, context)


