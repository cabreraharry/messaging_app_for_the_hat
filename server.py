import socket
from process import encrypt, decrypt
from utils import binary_to_string, string_to_binary, binary_to_hex, remove_trailing_zeros

# Server details (replace with your actual server IP/port)
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Function to receive data from the client
def receive_data():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((SERVER_HOST, SERVER_PORT))
        print("Server is listening for messages...")
        data, addr = s.recvfrom(1024)  # buffer size is 1024 bytes
        print(f"Received message from {addr}")

        # Split the received data into encrypted message and key using the ':' delimiter
        encrypted_message, key = data.decode().split(":")
        return encrypted_message, key

# Function to handle the received message
def handle_message(encrypted_message, key):
    # Decrypt the received message
    decrypted_message = remove_trailing_zeros(decrypt(encrypted_message, key))
    
    print("Received Encrypted Message: ", binary_to_string(encrypted_message))
    print("Received Key: ", key)
    
    print("Deciphertext in binary: \n", decrypted_message)
    print("Deciphered Hex: ", binary_to_hex(decrypted_message))
    print("Deciphered text: ", binary_to_string(decrypted_message))

    # Send the decrypted message back to the client (if needed)
    return binary_to_string(decrypted_message)

# Main function to run the server
def start_server():
    while True:
        # Receive the encrypted message and key
        encrypted_message, key = receive_data()

        # Process and decrypt the message
        decrypted_message = handle_message(encrypted_message, key)

        # Optionally send an acknowledgment back to the client (or decrypted message)
        print(f"Decrypted Message: {decrypted_message}\n")

if __name__ == '__main__':
    start_server()
