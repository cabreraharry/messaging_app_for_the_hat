from sort import sort_data
from hat import translate, rotate, reflect
from graph import graph_with_value, graph_with_coordinates, graph_hat
from utils import string_to_binary, binary_to_string, xor_bits, remove_trailing_zeros, calculate_diffusion, byte_to_enhanced_int
from data import data_list


def write(coordinates, bin):
    coordinates = sort_data(coordinates)
    flattened_data = [item for sublist in coordinates for item in sublist]
    bit_values = [bit for binary_string in bin for bit in binary_string]
    if len(bit_values) < len(flattened_data):
        bit_values.extend(['0'] * (len(flattened_data) - len(bit_values)))
    index_value_dict = [{coord: bit for coord, bit in zip(flattened_data[i:i+8], bit_values[i:i+8])} 
                    for i in range(0, len(flattened_data), 8)]
    index_value_dict = [d for d in index_value_dict if any(bit != '0' for bit in d.values())]
    
    return index_value_dict

def read(coordinates, index_value_dictionary):
    message = ""
    coordinates = sort_data(coordinates)
    for sublist in coordinates:
        sublist_message = ""
        all_zeros = True
        
        for coord in sublist:
            bit_found = '0'
            for dictionary in index_value_dictionary:
                if coord in dictionary:
                    bit_found = dictionary[coord]
                    break
                    
            sublist_message += bit_found

            if bit_found != '0':
                all_zeros = False

        message += sublist_message + " "
        
            
    return message


def combine_key(byte_list):
    byte_values = [int(b, 2) for b in byte_list]
    result = 0
    for byte in byte_values:
        result ^= byte
        result = ((result << 3) & 0xFF) | (result >> 5)
    
    return bin(result)[2:].zfill(8)



def transform(key_basis, data):
    transformed_data = data
    transformed_data = reflect(transformed_data)
    
    if key_basis[0:2] == '00':
        transformed_data = translate(transformed_data,1)
    elif key_basis[0:2] == '01':
        transformed_data = translate(transformed_data,1)
        transformed_data = translate(transformed_data,1)
    elif key_basis[0:2] == '10':
        transformed_data = translate(transformed_data,4)
    elif key_basis[0:2] == '11':
        transformed_data = translate(transformed_data,4)
        transformed_data = translate(transformed_data,4)
        
    if key_basis[2:4] == '00':
        translate(transformed_data,2)
    elif key_basis[2:4] == '01':
        transformed_data = translate(transformed_data,2)
        transformed_data = translate(transformed_data,2)
    elif key_basis[2:4] == '10':
        transformed_data = translate(transformed_data,5)
    elif key_basis[2:4] == '11':
        transformed_data = translate(transformed_data,5)
        transformed_data = translate(transformed_data,5)
        
    if key_basis[4:6] == '00':
        translate(transformed_data,3)
    elif key_basis[4:6] == '01':
        transformed_data = translate(transformed_data,3)
        transformed_data = translate(transformed_data,3)
    elif key_basis[4:6] == '10':
        transformed_data = translate(transformed_data,6)
    elif key_basis[4:6] == '11':
        transformed_data = translate(transformed_data,6)
        transformed_data = translate(transformed_data,6)
        
        
    rotation = (int(key_basis, 2) + int(key_basis[6:8], 2))%5
    transformed_data = rotate(transformed_data, rotation)
    return transformed_data
    


def reverse_transform(key_basis, data):
    transformed_data = data
        
    if key_basis[0:2] == '00':
        transformed_data = translate(transformed_data,4)
    elif key_basis[0:2] == '01':
        transformed_data = translate(transformed_data,4)
        transformed_data = translate(transformed_data,4)
    elif key_basis[0:2] == '10':
        transformed_data = translate(transformed_data,1)
    elif key_basis[0:2] == '11':
        transformed_data = translate(transformed_data,1)
        transformed_data = translate(transformed_data,1)
        
    if key_basis[2:4] == '00':
        transformed_data = translate(transformed_data,5)
    elif key_basis[2:4] == '01':
        transformed_data = translate(transformed_data,5)
        transformed_data = translate(transformed_data,5)
    elif key_basis[2:4] == '10':
        transformed_data = translate(transformed_data,2)
    elif key_basis[2:4] == '11':
        transformed_data = translate(transformed_data,2)
        transformed_data = translate(transformed_data,2)
        
    if key_basis[4:6] == '00':
        transformed_data = translate(transformed_data,6)
    elif key_basis[4:6] == '01':
        transformed_data = translate(transformed_data,6)
        transformed_data = translate(transformed_data,6)
    elif key_basis[4:6] == '10':
        transformed_data = translate(transformed_data,3)
    elif key_basis[4:6] == '11':
        transformed_data = translate(transformed_data,3)
        transformed_data = translate(transformed_data,3)
        
        
    rotation = 6 - (int(key_basis, 2) + int(key_basis[6:8], 2))%5
    transformed_data = rotate(transformed_data, rotation)
    
    transformed_data = reflect(transformed_data)

    return transformed_data


one_distributor = "11110000"

def encrypt(message, key):
    message_bin = string_to_binary(message).split(" ")
    if len(one_distributor) > 1:
        message_bin = xor_bits(message_bin, one_distributor,exclude_last=False)
    
    key_bin = string_to_binary(key).split(" ")
    
    xor = xor_bits(message_bin, key_bin)
    # xor = message_bin
    
    diffuser = calculate_diffusion(xor)
    combined_key = combine_key(key_bin)

    key_basis = xor_bits(combined_key, diffuser, exclude_last=False)
    
    data_index = byte_to_enhanced_int(combined_key, len(data_list))
    data = data_list[data_index]
    # graph_hat(data, f"Tesselation {data_index}")
            
    dict = write(data, xor)
    data = transform(key_basis[0], data)
    cipher_text = read(data, dict)
                
    return cipher_text


def decrypt(cipher, key):
    cipher_bin = cipher.split(" ")
    key_bin = string_to_binary(key).split(" ")
    
    diffuser = calculate_diffusion(cipher_bin)
    combined_key = combine_key(key_bin)
    
    key_basis = xor_bits(combined_key, diffuser, exclude_last=False)
    
    data_index = byte_to_enhanced_int(combined_key, len(data_list))
    data = data_list[data_index]    
    original_data = data
    
    data = transform(key_basis[0], data)
    dict = write(data, cipher_bin)
    
    data = reverse_transform(key_basis[0], data)
    original = remove_trailing_zeros(read(original_data, dict)).split(" ")
    
    xor = xor_bits(original, key_bin)
    if len(one_distributor) > 1:
        xor = xor_bits(xor, one_distributor, exclude_last=False)
    # xor = original
    
    
    return ' '.join(xor)