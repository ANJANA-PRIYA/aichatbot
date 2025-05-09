from flask import Flask, render_template, jsonify, request
import os
import os
print("Current Working Directory:", os.getcwd())


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get', methods=['POST'])
def get_response():
    print("Received request")
    data = request.form
    user_msg = data.get('msg', '')
    print(f"User said: {user_msg}")
    return jsonify({'text': f'You said: {user_msg}'})

@app.route('/api/get', methods=['POST'])
def get_response():
    data = request.form
    user_msg = data.get('msg', '')
    return jsonify({'text': f'You said: {user_msg}'})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

