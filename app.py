from flask import Flask, render_template, jsonify, request
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # This should be in the 'templates' folder

@app.route('/api/get', methods=['POST'])
def get_response():
    user_msg = request.form.get('msg', '')
    return jsonify({'response': f'You said: {user_msg}'})  # Use 'response' as the key

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
