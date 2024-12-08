import tkinter as tk
from tkinter import messagebox
import socket
from process import encrypt, decrypt
from utils import string_to_binary, binary_to_string, binary_to_hex, remove_trailing_zeros

# Server details (Replace with actual server IP/port)
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Function to send message
def send_message():
    message = message_entry.get()
    key = key_entry.get()

    if message == "" or key == "":
        messagebox.showerror("Input Error", "Message and Key are required")
        return

    # Encrypt the message
    print(f"Original message: {message}")
    encrypted_message = remove_trailing_zeros(encrypt(message, key))

    print("Ciphertext in binary: \n", encrypted_message)
    print("Ciphered Hex: ", binary_to_hex(encrypted_message), "\n\n")

    # Send the encrypted message and key to the server
    send_data(encrypted_message, key)

# Function to receive message
def receive_message():
    # Receive encrypted message and key from the server
    encrypted_message, key = receive_data()

    print(f"Received encrypted message: {binary_to_string(encrypted_message)}")
    print(f"Received key: {key}")

    # Decrypt the message
    decrypted_message = remove_trailing_zeros(decrypt(encrypted_message, key))

    print("Deciphertext in binary: \n", decrypted_message)
    print("Deciphered Hex: ", binary_to_hex(decrypted_message))
    print("Deciphered text: ", binary_to_string(decrypted_message))

    # Display the decrypted message
    messagebox.showinfo("Decrypted Message", binary_to_string(decrypted_message))

# Function to send encrypted message and key over the network
def send_data(encrypted_message, key):
    # Send the encrypted message and key with a ':' separator
    data_to_send = f"{encrypted_message}:{key}"
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(data_to_send.encode(), (SERVER_HOST, SERVER_PORT))

# Function to receive encrypted message and key from the network
def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        print("Waiting for messages...")
        data, addr = s.recvfrom(1024)  # buffer size is 1024 bytes
        print(f"Received message from {addr}")
        
        # Split the received data into encrypted message and key using the ':' delimiter
        encrypted_message, key = data.decode().split(":")
        return encrypted_message, key

# Create the GUI
root = tk.Tk()
root.title("Messaging App")

# Message Entry
message_label = tk.Label(root, text="Enter your message:")
message_label.pack()
message_entry = tk.Entry(root, width=50)
message_entry.pack()

# Key Entry
key_label = tk.Label(root, text="Enter encryption key:")
key_label.pack()
key_entry = tk.Entry(root, width=50)
key_entry.pack()

# Send Button
send_button = tk.Button(root, text="Send Message", command=send_message)
send_button.pack(pady=10)

# Receive Button
receive_button = tk.Button(root, text="Receive Message", command=receive_message)
receive_button.pack(pady=10)

root.mainloop()
