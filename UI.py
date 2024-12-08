import tkinter as tk
from tkinter import messagebox
import random
import string
from process import encrypt, decrypt
from utils import binary_to_string, remove_trailing_zeros, string_to_binary, binary_to_hex
from data import data_list

# Function to generate a random 16-character key
def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Function to encrypt the message
def encrypt_message():
    message = message_textbox.get("1.0", tk.END).strip()
    if len(message) > 64:
        messagebox.showerror("Input Error", "Message cannot be more than 64 characters!")
        return

    key = key_textbox.get() 
    if not message:
        messagebox.showerror("Input Error", "Message cannot be empty!")
        return
    if not key or len(key) != 16:
        messagebox.showerror("Input Error", "Key must be 16 characters long!")
        return

    # Encrypt the message and display results
    binary_message = string_to_binary(message)
    ciphertext = remove_trailing_zeros(encrypt(message, key, data_list))
    deciphertext = remove_trailing_zeros(decrypt(ciphertext, key, data_list))

    # Store encrypted data for later format switching
    result_data['ciphertext_binary'] = ciphertext
    result_data['ciphertext_hex'] = binary_to_hex(ciphertext)
    result_data['ciphertext_text'] = binary_to_string(ciphertext)

    show_ciphertext()  # Initially display text format

# Function to decrypt the ciphertext
def decrypt_message():
    ciphertext = result_data.get(f'ciphertext_{current_format}', "")  
    key = key_textbox.get()  # Get the key from the textbox
    
    if not ciphertext:
        messagebox.showerror("Input Error", "No ciphertext to decrypt!")
        return
    if not key or len(key) != 16:
        messagebox.showerror("Input Error", "Key must be 16 characters long!")
        return

    # Decrypt the ciphertext and display the result
    try:
        binary_ciphertext = string_to_binary(ciphertext) if current_format == "text" else ciphertext
        decrypted_message = decrypt(binary_ciphertext, key, data_list)
        decrypted_textbox.delete(1.0, tk.END)
        decrypted_textbox.insert(tk.END, binary_to_string(remove_trailing_zeros(decrypted_message)))
    except Exception as e:
        messagebox.showerror("Decryption Error", f"Failed to decrypt the message: {str(e)}")

# Function to show the ciphertext in the selected format
def show_ciphertext():
    result_ciphertext.delete(1.0, tk.END)
    result_ciphertext.insert(tk.END, result_data[f'ciphertext_{current_format}'])

# Function to toggle the format
def toggle_format():
    global current_format
    current_format = format_var.get()  # Get the selected format from radio button
    show_ciphertext()

# Function to set the generated key in the key textbox
def display_generated_key():
    message = message_textbox.get("1.0", tk.END).strip()  # Get the current message
    key = generate_key()
    
    # Ensure the last character of the key is not the same as the message's last character
    while message and key[-1] == message[-1]:
        key = generate_key()
    
    key_textbox.delete(0, tk.END)
    key_textbox.insert(0, key)

# Initialize the format and result_data dictionary
current_format = 'text'  # Default format is text
result_data = {}

# Setting up the Tkinter window
root = tk.Tk()
root.title("Encrypt/Decrypt Message")

# Set window size (portrait orientation)
root.geometry("600x500")

# Message Textbox (Limit to 64 chars)
message_label = tk.Label(root, text="Enter message (max 64 chars):")
message_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

# Adjust width of the message textbox to match the key textbox + button width
message_textbox = tk.Text(root, height=1, width=40)  # Adjusted width
message_textbox.grid(row=0, column=1, columnspan=2, padx=10, pady=5)

# Key Textbox
key_label = tk.Label(root, text="Generated Key (16 characters):")
key_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

key_textbox = tk.Entry(root, width=20)
key_textbox.grid(row=1, column=1, padx=10, pady=5)

# Button to generate key
generate_key_button = tk.Button(root, text="Generate Key", command=display_generated_key)
generate_key_button.grid(row=1, column=2, padx=10, pady=5)

# Button to encrypt message
encrypt_button = tk.Button(root, text="Encrypt Message", command=encrypt_message)
encrypt_button.grid(row=2, column=1, pady=10)

# Radio Buttons for format selection (Text, Hex, Binary)
format_var = tk.StringVar(value='text')  # Default format is text

radio_frame = tk.Frame(root)
radio_frame.grid(row=3, column=0, columnspan=3, pady=5)

text_radio = tk.Radiobutton(radio_frame, text="Text", variable=format_var, value='text', command=toggle_format)
text_radio.grid(row=0, column=0, padx=5)

hex_radio = tk.Radiobutton(radio_frame, text="Hex", variable=format_var, value='hex', command=toggle_format)
hex_radio.grid(row=0, column=1, padx=5)

binary_radio = tk.Radiobutton(radio_frame, text="Binary", variable=format_var, value='binary', command=toggle_format)
binary_radio.grid(row=0, column=2, padx=5)

# Result Display for Ciphertext
result_ciphertext_label = tk.Label(root, text="Ciphertext:")
result_ciphertext_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

# Ciphertext display area
result_ciphertext = tk.Text(root, height=1, width=40)  # Adjusted height
result_ciphertext.grid(row=5, column=0, columnspan=3, padx=10, pady=5)

# Button to decrypt message
decrypt_button = tk.Button(root, text="Decrypt Message", command=decrypt_message)
decrypt_button.grid(row=6, column=1, pady=10)

# Decrypted Output
decrypted_label = tk.Label(root, text="Decrypted Output:")
decrypted_label.grid(row=7, column=0, padx=10, pady=5, sticky="w")

decrypted_textbox = tk.Text(root, height=1, width=40)
decrypted_textbox.grid(row=8, column=0, columnspan=3, padx=10, pady=5)

# Start the Tkinter event loop
root.mainloop()
