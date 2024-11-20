from flask import Flask, request, jsonify
from cryptography.fernet import Fernet
from flask_cors import CORS



app = Flask(__name__)
CORS(app)

# Generate or use a predefined encryption key
encryption_key = Fernet.generate_key()
cipher = Fernet(encryption_key)

# Temporary storage for messages
messages = []

@app.route('/send', methods=['POST'])
def send_message():
    try:
        data = request.json
        message = data.get("message", "")
        encrypted_message = cipher.encrypt(message.encode())
        messages.append(encrypted_message)
        return jsonify({"status": "success", "encrypted_message": encrypted_message.decode()}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/receive', methods=['GET'])
def receive_messages():
    try:
        decrypted_messages = [cipher.decrypt(msg).decode() for msg in messages]
        return jsonify({"status": "success", "messages": decrypted_messages}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
