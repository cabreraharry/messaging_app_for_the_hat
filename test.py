from process import encrypt, decrypt
from utils import binary_to_string, remove_trailing_zeros, byte_to_enhanced_int
from data import data_list
import random
import string

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def test_accuracy(num=100):
    invalid_counter = 0
    for i in range(num):
        # plaintext = random_string(random.randint(10, 20))
        plaintext = random_string(128)
        key = random_string(16) 

        ciphertext = remove_trailing_zeros(encrypt(plaintext, key))
        deciphertext = remove_trailing_zeros(decrypt(ciphertext, key))

        message = binary_to_string(deciphertext)
        
        print(plaintext, " - ",key,"\n")
        if plaintext != message:
            print("Invalid")
            invalid_counter += 1

    print(invalid_counter)
    
test_accuracy(100)

# Max plaintext tester result: 230

# for num in range(200, 256):
#     for i in range(10):
#         # plaintext = random_string(random.randint(10, 20))
#         plaintext = random_string(num)
#         key = random_string(16) 

#         ciphertext = remove_trailing_zeros(encrypt(plaintext, key, data_list))
#         deciphertext = remove_trailing_zeros(decrypt(ciphertext, key, data_list))

#         message = binary_to_string(deciphertext)
        
#         if plaintext != message:
#             invalid_counter += 1
    
#     if invalid_counter > 0:
#         print(f"length: {num} - number of invalid: {invalid_counter}")
#     else:
#         print(f"passed {num}")

# print(invalid_counter)