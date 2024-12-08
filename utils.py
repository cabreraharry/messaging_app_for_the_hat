import random
import string

def generate_key(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def string_to_binary(input_string):
    binary_representation = ' '.join(format(ord(char), '08b') for char in input_string)
    return binary_representation

def binary_to_string(binary_str):
    chars = binary_str.split()
    actual_string = ''.join([chr(int(char, 2)) for char in chars])
    return actual_string

def binary_to_hex(binary_str):
    binary_groups = binary_str.split()
    hex_string = ' '.join([format(int(group, 2), '02X') for group in binary_groups])
    return hex_string


def calculate_diffusion(input_bits):
    if isinstance(input_bits, str):
        input_bits = input_bits.replace(" ", "")
    elif isinstance(input_bits, list):
        input_bits = "".join(input_bits)

    ones_count = input_bits.count('1')

    enhanced_count = (ones_count * 73) ^ 137

    diffusion_string = f"{enhanced_count % 256:08b}"

    return diffusion_string


def byte_to_enhanced_int(byte, max):
    int_value = int(byte, 2)
    int_value *= 31
    int_value ^= 55
    return int_value % max
    


def xor_bits(message, key, exclude_last=True):
    # Ensure the message is a list of binary strings
    if isinstance(message, str):
        # Split the string into a list of 8-bit binary strings
        message = message.split()
    elif not all(len(binary) == 8 for binary in message):
        raise ValueError("Each binary string in the list must be 8 bits long.")

    # Ensure the key is a list of binary strings
    if isinstance(key, str):
        key = key.split()
    elif not all(len(binary) == 8 for binary in key):
        raise ValueError("Each binary string in the key must be 8 bits long.")

    # Perform XOR operation
    key_len = len(key)
    result = []

    # Determine if the last byte should be excluded from XOR
    if exclude_last:
        # XOR all except the last byte
        for i, binary in enumerate(message[:-1]):
            key_binary = key[i % key_len]
            xor_result = ''.join(str(int(a) ^ int(b)) for a, b in zip(binary, key_binary))
            result.append(xor_result)
        # Include the last byte without XOR
        result.append(message[-1])
    else:
        # XOR all bytes as usual
        for i, binary in enumerate(message):
            key_binary = key[i % key_len]
            xor_result = ''.join(str(int(a) ^ int(b)) for a, b in zip(binary, key_binary))
            result.append(xor_result)

    return result




def remove_leading_zeros(binary_string):
    binary_string = binary_string.replace(" 00000000", "")
    return binary_string


def remove_trailing_zeros(binary_string):
    parts = binary_string.split()
    while parts and parts[-1] == "00000000":
        parts.pop()
    return " ".join(parts)