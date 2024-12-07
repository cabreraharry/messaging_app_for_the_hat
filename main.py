from process import encrypt, decrypt
from utils import binary_to_string, remove_trailing_zeros, string_to_binary, binary_to_hex
from data import data_list


# message  = "Elsid Rick L Panolino"
# key = "23124ersb"

message = input("Enter message: ")
key = input("Enter key: ")

print("Original message in binary:\n", string_to_binary(message))
print("Original message: ", message, "\n")

ciphertext = remove_trailing_zeros(encrypt(message, key))
deciphertext = remove_trailing_zeros(decrypt(ciphertext, key))

print("Ciphertext in binary: \n",ciphertext)
print("Ciphered Hex: ",binary_to_hex(ciphertext),"\n\n")
print("Ciphered text: ",binary_to_string(ciphertext),"\n\n")

print("Deciphertext in binary: \n",deciphertext)
print("Deciphered Hex: ",binary_to_hex(deciphertext))
print("Deciphered text: ",binary_to_string(deciphertext))