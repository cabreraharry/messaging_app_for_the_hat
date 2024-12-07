import numpy as np
from math import log2
import matplotlib.pyplot as plt
from scipy.stats import chisquare

from process import encrypt, decrypt
from data import data_list
from utils import remove_trailing_zeros

from metrics_batch import random_string, alternative_text


# Function to calculate entropy for hexadecimal pairs
def calculate_entropy_hex(hex_data):
    # Split the hex string into 2-character chunks
    hex_pairs = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
    frequency = {pair: hex_pairs.count(pair) / len(hex_pairs) for pair in set(hex_pairs)}
    entropy = -sum(p * log2(p) for p in frequency.values())
    return entropy


# Function for frequency analysis of hex pairs
def frequency_analysis(hex_data):
    # Split the hex string into 2-character chunks
    hex_pairs = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
    frequency = {pair: hex_pairs.count(pair) for pair in set(hex_pairs)}
    return frequency


def plot_frequency(frequency):
    plt.bar(frequency.keys(), frequency.values())
    plt.xlabel('Hex Pairs')
    plt.ylabel('Frequency')
    plt.title('Frequency Analysis of Ciphertext (Hex Pairs)')
    plt.show()


# Function to calculate Hamming distance between two hex strings
def hamming_distance_hex(hex1, hex2):
    # Pad the shorter hex string with leading zeroes to make both strings equal length
    max_len = max(len(hex1), len(hex2))
    hex1 = hex1.zfill(max_len)
    hex2 = hex2.zfill(max_len)
    
    # Convert each 2-character hex pair to binary and calculate the XOR
    distance = 0
    for i in range(0, len(hex1), 2):
        pair1 = hex1[i:i+2]
        pair2 = hex2[i:i+2]
        
        # Ensure that we're not encountering an empty pair
        if pair1 and pair2:
            distance += bin(int(pair1, 16) ^ int(pair2, 16)).count('1')
        else:
            raise ValueError("Invalid hex pair encountered during Hamming distance calculation.")
    
    return distance



# Function to calculate avalanche effect
def avalanche_effect(hex1, hex2):
    distance = hamming_distance_hex(hex1, hex2)
    bit_difference = (distance / (len(hex1) * 4)) * 100  # Percentage of differing bits
    return bit_difference


# Chi-square test for uniform distribution in hex pairs
def chi_square_test(hex_data):
    # Split the hex string into 2-character chunks
    hex_pairs = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
    observed = [hex_pairs.count(pair) for pair in set(hex_pairs)]
    expected = [len(hex_pairs) / len(set(hex_pairs))] * len(set(hex_pairs))
    chi_stat, p_value = chisquare(observed, f_exp=expected)
    return chi_stat, p_value


# Function to calculate correlation between plaintext and ciphertext (in hex pairs)
def calculate_correlation_hex(plaintext, ciphertext_hex):
    # Convert plaintext to hexadecimal representation
    plaintext_hex = plaintext.encode('utf-8').hex()
    
    # Split hex strings into 2-character chunks
    plain_hex_pairs = [plaintext_hex[i:i+2] for i in range(0, len(plaintext_hex), 2)]
    cipher_hex_pairs = [ciphertext_hex[i:i+2] for i in range(0, len(ciphertext_hex), 2)]
    
    # Get the set of unique hex pairs from both plaintext and ciphertext
    all_pairs = sorted(set(plain_hex_pairs) | set(cipher_hex_pairs))
    
    # Calculate frequency of each pair in both plaintext and ciphertext
    plain_freq = np.array([plain_hex_pairs.count(pair) for pair in all_pairs])
    cipher_freq = np.array([cipher_hex_pairs.count(pair) for pair in all_pairs])
    
    # Normalize the frequencies by dividing by the total count
    plain_freq = plain_freq / np.sum(plain_freq)
    cipher_freq = cipher_freq / np.sum(cipher_freq)
    
    # Calculate the correlation coefficient
    correlation = np.corrcoef(plain_freq, cipher_freq)
    return correlation[0, 1]


def binary_to_hex(binary_string):
    # Remove spaces from the binary string
    binary_string = binary_string.replace(" ", "")
    
    # Ensure the length of binary_string is a multiple of 4 for correct hex conversion
    binary_string = binary_string.zfill(len(binary_string) + (4 - len(binary_string) % 4) % 4)
    
    # Convert binary string to hexadecimal
    hex_string = hex(int(binary_string, 2))[2:]  # Remove "0x" prefix
    return hex_string.zfill(len(binary_string) // 4)  # Pad with zeroes if necessary




# Main function to accept inputs and calculate all metrics
def main():
    # Input plain text, key, ciphertext, and alternative key/ciphertext
    # plaintext = input("Enter the plain text: ")
    plaintext = random_string(128)
    
    # key = input("Enter the encryption key: ")
    key = random_string(16)
    
    ciphertext = remove_trailing_zeros(encrypt(plaintext, key, data_list))
    
    # alt_key = input("Enter the alternative encryption key: ")
    alt_key = alternative_text(key)
    
    alt_ciphertext = remove_trailing_zeros(encrypt(plaintext, alt_key, data_list))
    
    # Convert binary ciphertext to hexadecimal
    ciphertext_hex = binary_to_hex(ciphertext)
    print(ciphertext_hex)
    alt_ciphertext_hex = binary_to_hex(alt_ciphertext)
    print(alt_ciphertext_hex)
    
    # 1. Entropy calculation
    entropy = calculate_entropy_hex(ciphertext_hex)
    print("Entropy of the ciphertext (hex pairs):", entropy)
    
    # 2. Frequency analysis and plotting
    freq = frequency_analysis(ciphertext_hex)
    plt.figure()
    plot_frequency(freq)
    
    # 3. Avalanche effect testing
    avalanche = avalanche_effect(ciphertext_hex, alt_ciphertext_hex)
    print(f"Avalanche Effect: {avalanche:.2f}%")
    
    # 4. Chi-Square Test
    chi_stat, p_value = chi_square_test(ciphertext_hex)
    print(f"Chi-Square Statistic: {chi_stat}, p-value: {p_value}")
    
    # 5. Plaintext-Ciphertext Correlation
    correlation = calculate_correlation_hex(plaintext, ciphertext_hex)
    print("Plaintext-Ciphertext Correlation:", correlation)
    
    
    # 6. Key Sensitivity Test
    key_diff_avalanche = avalanche_effect(ciphertext_hex, alt_ciphertext_hex)
    print(f"Key Sensitivity Avalanche Effect: {key_diff_avalanche:.2f}%")


if __name__ == "__main__":
    main()
