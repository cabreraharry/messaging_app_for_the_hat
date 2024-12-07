import tkinter as tk
from tkinter import messagebox
import random
import string
import requests
from process import encrypt, decrypt  # assuming these are your encryption/decryption methods
from utils import binary_to_string, binary_to_hex

# Flask server URL
SERVER_URL = "http://127.0.0.1:5000"

# Function to generate a random 16-character key
def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Function to encrypt the message and send it to the server
def encrypt_message():
    message = message_textbox.get("1.0", tk.END).strip()
    if len(message) > 64:
        messagebox.showerror("Input Error", "Message cannot be more than 64 characters!")
        return

    key = generate_key()
    
    if not message:
        messagebox.showerror("Input Error", "Message cannot be empty!")
        return

    # Encrypt the message by sending it to the Flask server
    try:
        response = requests.post(f"{SERVER_URL}/send_message", json={"message": message, "key": key})
        response_data = response.json()
        
        if response.status_code == 200:
            encrypted_message = response_data.get('encrypted_message', '')
            
            # Decrypt the message using the developed decryption algorithm
            decrypted_message_binary = decrypt(encrypted_message, key)
            
            # Convert binary to string (the decrypted message is binary)
            decrypted_message = binary_to_string(decrypted_message_binary)
            
            # Show the decrypted message in the received message box
            received_message_textbox.delete("1.0", tk.END)
            received_message_textbox.insert(tk.END, decrypted_message)
        else:
            messagebox.showerror("Encryption Error", response_data.get("error", "Unknown Error"))
    
    except Exception as e:
        messagebox.showerror("Network Error", f"Failed to send message: {str(e)}")

# Create main window
root = tk.Tk()
root.title("Encrypted Messaging")

# Create text box for entering the message
message_label = tk.Label(root, text="Enter your message:")
message_label.pack(pady=5)

message_textbox = tk.Text(root, height=5, width=40)
message_textbox.pack(pady=10)

# Send Button
send_button = tk.Button(root, text="Send", width=20, command=encrypt_message)
send_button.pack(pady=10)

# Create text box for received message (decrypted)
received_message_label = tk.Label(root, text="Received message:")
received_message_label.pack(pady=5)

received_message_textbox = tk.Text(root, height=5, width=40)
received_message_textbox.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
