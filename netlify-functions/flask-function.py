from flask import Flask
from serverless import handler

# Create the Flask app
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, world!"

# Adapt the Flask app to be a serverless function
def lambda_handler(event, context):
    return handler(app, event, context)
