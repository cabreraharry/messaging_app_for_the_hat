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
def send_message():
    message = message_textbox.get("1.0", tk.END).strip()
    
    if not message:
        messagebox.showerror("Input Error", "Message cannot be empty!")
        return
    
    key = generate_key()
    
    # Encrypt the message
    try:
        response = requests.post(f"{SERVER_URL}/send_message", json={"message": message, "key": key})
        response_data = response.json()
        
        if response.status_code == 200:
            encrypted_message = response_data.get('encrypted_message', '')
            
            # Add the message to the chat (encrypted for sending)
            add_message_to_chat(message, encrypted=True)
            
            # Send the encrypted message for decryption and display the result
            receive_message(encrypted_message, key)
        else:
            messagebox.showerror("Encryption Error", response_data.get("error", "Unknown Error"))
    
    except Exception as e:
        messagebox.showerror("Network Error", f"Failed to send message: {str(e)}")

# Function to receive and decrypt the message
def receive_message(encrypted_message, key):
    try:
        response = requests.post(f"{SERVER_URL}/receive_message", json={"encrypted_message": encrypted_message, "key": key})
        response_data = response.json()
        
        if response.status_code == 200:
            decrypted_message = response_data.get('decrypted_message', '')
            
            # Add the decrypted message to the chat (this simulates another user receiving it)
            add_message_to_chat(decrypted_message, encrypted=False)
        else:
            messagebox.showerror("Decryption Error", response_data.get("error", "Unknown Error"))
    
    except Exception as e:
        messagebox.showerror("Network Error", f"Failed to receive message: {str(e)}")

# Function to add a message to the chat box
def add_message_to_chat(message, encrypted=False):
    # Determine whether the message is encrypted or decrypted and format accordingly
    if encrypted:
        message = f"Encrypted: {message}"  # For demonstration purposes
    # Add the message to the UI's chat window
    chat_window.insert(tk.END, f"{'You' if encrypted else 'Friend'}: {message}\n")
    chat_window.yview(tk.END)  # Scroll to the bottom

    # Clear the input textbox
    message_textbox.delete("1.0", tk.END)

# Create main window
root = tk.Tk()
root.title("Encrypted Messaging App")
root.geometry("400x500")

# Create a scrollable chat window
chat_window_frame = tk.Frame(root)
chat_window_frame.pack(pady=10)

chat_window = tk.Text(chat_window_frame, height=15, width=50, wrap=tk.WORD, state=tk.DISABLED)
chat_window.pack()

# Create text box for entering the message
message_label = tk.Label(root, text="Type your message:")
message_label.pack(pady=5)

message_textbox = tk.Text(root, height=5, width=40)
message_textbox.pack(pady=10)

# Send Button
send_button = tk.Button(root, text="Send", width=20, command=send_message)
send_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
