import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from process import encrypt, decrypt
from utils import binary_to_string, remove_trailing_zeros, string_to_binary, binary_to_hex
import random
import string

def generate_key(length=16):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(length))

def show_message_details(message, key, is_sent=True):
    """ Display message details in the terminal (key, binary, ciphertext, etc.) """
    # Original message in binary
    message_binary = string_to_binary(message)
    
    # Encrypt the message
    ciphertext = encrypt(message, key)
    ciphertext_binary = remove_trailing_zeros(ciphertext)
    encrypted_message = binary_to_string(ciphertext_binary)
    
    # Convert ciphertext to hex
    ciphertext_hex = binary_to_hex(ciphertext_binary)

    # Display details in the terminal
    print(f"\n{'Sent' if is_sent else 'Received'} message:")
    print(f"Original message in binary:\n{' '.join(message_binary)}")
    print(f"Original message: {message}")
    print(f"\nGenerated Key: {key}")
    print(f"\nCiphertext in binary:\n{' '.join(ciphertext_binary)}")
    print(f"Ciphered Hex: {ciphertext_hex}")
    print(f"\nCiphered text: {encrypted_message}")

    # Decrypt the message for received side
    if not is_sent:
        deciphertext = remove_trailing_zeros(decrypt(ciphertext_binary, key))
        decrypted_message = binary_to_string(deciphertext)
        decrypted_hex = binary_to_hex(deciphertext)
        print(f"\nDeciphertext in binary:\n{' '.join(deciphertext)}")
        print(f"Deciphered Hex: {decrypted_hex}")
        print(f"Deciphered text: {decrypted_message}")
    
def receive_message(client_socket, text_area):
    while True:
        try:
            # Receive the key and ciphertext from the server
            key_and_ciphertext = client_socket.recv(1024).decode()
            if key_and_ciphertext:
                key, ciphertext = key_and_ciphertext.split(':', 1)  # Split key and message
                ciphertext_binary = string_to_binary(ciphertext)  # Convert ciphertext to binary
                deciphertext = remove_trailing_zeros(decrypt(ciphertext_binary, key))  # Decrypt the message
                decrypted_message = binary_to_string(deciphertext)  # Convert binary back to text

                # Display the received message on the UI
                text_area.insert(tk.END, f"Friend: {decrypted_message}\n")
                text_area.yview(tk.END)  # Automatically scroll to the bottom

                # Show message details in the terminal (key, binary, ciphertext, etc.)
                show_message_details(decrypted_message, key, is_sent=False)
        except Exception as e:
            print(f"Error while receiving message: {e}")
            break

def send_message(client_socket, message, text_area):
    # Generate a new key for this message
    key = generate_key()
    message_binary = string_to_binary(message)  # Convert the message to binary
    ciphertext = encrypt(message, key)  # Encrypt the message
    ciphertext_binary = remove_trailing_zeros(ciphertext)  # Remove trailing zeros
    encrypted_message = binary_to_string(ciphertext_binary)  # Convert ciphertext to string
    client_socket.send(f"{key}:{encrypted_message}".encode())  # Send the key and encrypted message over the network

    # Display the sent message on the UI
    text_area.insert(tk.END, f"You: {message}\n")
    text_area.yview(tk.END)  # Automatically scroll to the bottom

    # Show message details in the terminal (key, binary, ciphertext, etc.)
    show_message_details(message, key, is_sent=True)

def server_program(text_area):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 12345))  # Bind to the IP address and port
    server_socket.listen(1)
    print("Waiting for a connection...")
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")
    text_area.insert(tk.END, f"Connection established with {client_address}\n")
    
    # Start a new thread to receive messages
    threading.Thread(target=receive_message, args=(client_socket, text_area), daemon=True).start()

    return client_socket  # Return the client socket for use in sending messages

def client_program(text_area, server_ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, 12345))  # Connect to the server on the same port
    print("Connected to server.")
    
    # Start a new thread to receive messages
    threading.Thread(target=receive_message, args=(client_socket, text_area), daemon=True).start()

    return client_socket  # Return the client socket for use in sending messages

def on_send_button_click(client_socket, text_area, message_entry):
    message = message_entry.get()
    if message:
        send_message(client_socket, message, text_area)  # Send encrypted message
        message_entry.delete(0, tk.END)  # Clear the message input box

def start_app(is_server, server_ip=None):
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
    send_button = tk.Button(root, text="Send", width=15, command=lambda: on_send_button_click(client_socket, text_area, message_entry))
    send_button.pack(padx=10, pady=5)

    # Initialize client_socket variable outside the threading
    client_socket = None

    # If server mode, set up server
    if is_server:
        client_socket = server_program(text_area)
    else:
        client_socket = client_program(text_area, server_ip)

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
