import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from process import encrypt, decrypt
from utils import binary_to_string, remove_trailing_zeros, string_to_binary, binary_to_hex
import random
import string

# Function to generate a random key (you can adjust the key size)
def generate_key(length=16):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

# Function to handle receiving messages over the network
def receive_message(client_socket, text_area, key):
    while True:
        try:
            ciphertext = client_socket.recv(1024).decode()  # Receive the encrypted message
            if ciphertext:
                # Decrypt the message
                ciphertext_binary = string_to_binary(ciphertext)  # Convert ciphertext to binary
                deciphertext = remove_trailing_zeros(decrypt(ciphertext_binary, key))  # Decrypt the message
                decrypted_message = binary_to_string(deciphertext)  # Convert binary back to text

                # Display the decrypted message in the chat window
                text_area.insert(tk.END, f"Friend: {decrypted_message}\n")
                text_area.yview(tk.END)  # Automatically scroll to the bottom
        except Exception as e:
            print(f"Error while receiving message: {e}")
            break

# Function to send the encrypted message
def send_message(client_socket, message, text_area, key):
    message_binary = string_to_binary(message)
    ciphertext = encrypt(message, key)
    ciphertext_binary = remove_trailing_zeros(ciphertext)
    encrypted_message = binary_to_string(ciphertext_binary)
    client_socket.send(encrypted_message.encode())
    text_area.insert(tk.END, f"You: {message}\n")
    text_area.yview(tk.END)

# Function to set up the server (receiver)
def server_program(text_area, key):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Listen on port 12345
    server_socket.listen(1)
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")
    text_area.insert(tk.END, f"Connection established with {client_address}\n")
    
    # Start a new thread for receiving messages
    threading.Thread(target=receive_message, args=(client_socket, text_area, key), daemon=True).start()

    return client_socket  # Return the client socket for use in sending messages

# Function to set up the client (sender)
def client_program(text_area, key, server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 12345))  # Connect to the server on the same port
    print("Connected to server.")
    
    # Start a new thread for receiving messages
    threading.Thread(target=receive_message, args=(client_socket, text_area, key), daemon=True).start()

    return client_socket  # Return the client socket for use in sending messages

# Function to send message when the "Send" button is clicked
def on_send_button_click(client_socket, text_area, key, message_entry):
    message = message_entry.get()
    if message:
        send_message(client_socket, message, text_area, key)
        message_entry.delete(0, tk.END)  # Clear the message input box

# Function to start the application (either server or client mode)
def start_app(is_server, server_ip=None):
    # Generate a key for encryption
    key = generate_key()

    # Set up the UI window
    root = tk.Tk()
    root.title("Encrypted Messenger")

    # Create a text area for displaying messages
    text_area = scrolledtext.ScrolledText(root, width=50, height=15, wrap=tk.WORD)
    text_area.pack(padx=10, pady=10)

    # Create a message entry box
    message_entry = tk.Entry(root, width=40)
    message_entry.pack(padx=10, pady=5)

    # Create a "Send" button
    send_button = tk.Button(root, text="Send", width=15, command=lambda: on_send_button_click(client_socket, text_area, key, message_entry))
    send_button.pack(padx=10, pady=5)

    # Initialize client_socket variable outside the threading
    client_socket = None

    # If server mode, set up server
    if is_server:
        client_socket = server_program(text_area, key)
    else:
        client_socket = client_program(text_area, key, server_ip)
    
    # Run the UI
    root.mainloop()

if __name__ == "__main__":
    mode = input("Enter 'server' to start as a server, or 'client' to start as a client: ").strip().lower()
    if mode == 'server':
        start_app(is_server=True)
    elif mode == 'client':
        server_ip = input("Enter the server IP address: ").strip()
        start_app(is_server=False, server_ip=server_ip)
    else:
        print("Invalid mode.")