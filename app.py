from flask import Flask, request, jsonify
from process import encrypt, decrypt
from utils import binary_to_string, remove_trailing_zeros
import random
import string

app = Flask(__name__)

# Function to generate a random 16-character key
def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '')
    key = data.get('key', '')
    
    if not message or not key:
        return jsonify({"error": "Message and key are required!"}), 400
    
    if len(message) > 64:
        return jsonify({"error": "Message cannot be more than 64 characters!"}), 400
    
    try:
        encrypted_message = encrypt(message, key)
        return jsonify({"encrypted_message": encrypted_message})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/receive_message', methods=['POST'])
def receive_message():
    data = request.json
    encrypted_message = data.get('encrypted_message', '')
    key = data.get('key', '')
    
    if not encrypted_message or not key:
        return jsonify({"error": "Encrypted message and key are required!"}), 400

    try:
        decrypted_message = decrypt(encrypted_message, key)
        return jsonify({"decrypted_message": decrypted_message})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
