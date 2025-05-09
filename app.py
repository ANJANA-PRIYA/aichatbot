from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get', methods=['POST'])  # Use POST method
def get_response():
    data = request.get_json()  # Read JSON from frontend
    user_msg = data.get('msg', '')
    return jsonify({'response': f'You said: {user_msg}'})  # Respond with JSON

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
