import tkinter as tk
from tkinter import messagebox
import random
import string
import requests
from process import encrypt, decrypt
from utils import binary_to_string, binary_to_hex


SERVER_URL = "http://127.0.0.1:5000"


def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    

def send_message():
    message = message_textbox.get("1.0", tk.END).strip()
    if not message:
        messagebox.showerror("Input Error", "Message cannot be empty!")
        return
    
    key = generate_key()
    encrypted_message = encrypt(message, key)
    
    try:
        response = requests.post(f"{SERVER_URL}/send_message", json={
            "encrypted_message": encrypted_message,
            "key": key
        })

        response_data = response.json()
        if response.status_code == 200:
            add_message_to_chat(encrypted_message, encrypted=True)
        else:
            messagebox.showerror("Encryption Error", response_data.get("error", "Unknown Error"))
    except Exception as e:
        messagebox.showerror("Network Error", f"Failed to send message: {str(e)}")
    finally:
        message_textbox.delete("1.0", tk.END)



def receive_message(encrypted_message, key):
    """Decrypt a received message and display it."""
    try:
        response = requests.post(f"{SERVER_URL}/receive_message", json={
            "encrypted_message": encrypted_message,
            "key": key
        })

        try:
            response_data = response.json()
        except ValueError:
            messagebox.showerror("Response Error", "Invalid response from server.")
            return
        
        if response.status_code == 200:
            decrypted_message = response_data.get('decrypted_message', '')
            add_message_to_chat(decrypted_message, encrypted=False)
        else:
            messagebox.showerror("Decryption Error", response_data.get("error", "Unknown Error"))
    except Exception as e:
        messagebox.showerror("Network Error", f"Failed to receive message: {str(e)}")



def add_message_to_chat(message, encrypted=False):
    """Add a message to the chat window."""
    display_message = f"{'Encrypted' if encrypted else 'Friend'}: {message}"

    chat_window.config(state=tk.NORMAL)  
    chat_window.insert(tk.END, f"{display_message}\n")
    chat_window.yview(tk.END)  
    chat_window.config(state=tk.DISABLED)  


root = tk.Tk()
root.title("Encrypted Messaging App")
root.geometry("400x500")

chat_window_frame = tk.Frame(root)
chat_window_frame.pack(pady=10)

chat_window = tk.Text(chat_window_frame, height=15, width=50, wrap=tk.WORD, state=tk.DISABLED)
chat_window.pack()

message_label = tk.Label(root, text="Type your message:")
message_label.pack(pady=5)

message_textbox = tk.Text(root, height=5, width=40)
message_textbox.pack(pady=10)

send_button = tk.Button(root, text="Send", width=20, command=send_message)
send_button.pack(pady=10)

root.mainloop()