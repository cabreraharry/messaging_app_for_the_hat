import numpy as np
import random
import string
from math import log2
import matplotlib.pyplot as plt
from scipy.stats import chisquare
from process import encrypt, decrypt
from utils import remove_trailing_zeros
import csv


# Helper function to generate random strings for plaintext and keys
def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Function to alter some characters in a string
def alternative_text(s, min_modifications=5, max_modifications=8):
    if len(s) < max_modifications:
        max_modifications = len(s)

    num_modifications = random.randint(min_modifications, max_modifications)

    s_list = list(s)

    for _ in range(num_modifications):
        index = random.randint(0, len(s) - 1)
        s_list[index] = random.choice(string.ascii_letters + string.digits)

    return ''.join(s_list)

# Function to calculate entropy for hexadecimal pairs
def calculate_entropy_hex(hex_data):
    hex_pairs = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
    frequency = {pair: hex_pairs.count(pair) / len(hex_pairs) for pair in set(hex_pairs)}
    entropy = -sum(p * log2(p) for p in frequency.values())
    return entropy


# Frequency analysis of hex pairs
def frequency_analysis(hex_data):
    hex_pairs = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
    frequency = {pair: hex_pairs.count(pair) for pair in set(hex_pairs)}
    return frequency


def plot_frequency(frequency):
    plt.bar(frequency.keys(), frequency.values())
    plt.xlabel('Hex Pairs')
    plt.ylabel('Frequency')
    plt.title('Frequency Analysis of Ciphertext (Hex Pairs)')
    plt.show()


# Calculate Hamming distance between two hex strings
def hamming_distance_hex(hex1, hex2):
    max_len = max(len(hex1), len(hex2))
    hex1 = hex1.zfill(max_len)
    hex2 = hex2.zfill(max_len)
    distance = 0
    for i in range(0, len(hex1), 2):
        pair1 = hex1[i:i+2]
        pair2 = hex2[i:i+2]
        if pair1 and pair2:
            distance += bin(int(pair1, 16) ^ int(pair2, 16)).count('1')
        else:
            raise ValueError("Invalid hex pair encountered during Hamming distance calculation.")
    return distance


# Calculate avalanche effect
def avalanche_effect(hex1, hex2):
    distance = hamming_distance_hex(hex1, hex2)
    bit_difference = (distance / (len(hex1) * 4)) * 100
    return bit_difference


# Chi-square test for uniform distribution in hex pairs
def chi_square_test(hex_data):
    hex_pairs = [hex_data[i:i+2] for i in range(0, len(hex_data), 2)]
    observed = [hex_pairs.count(pair) for pair in set(hex_pairs)]
    expected = [len(hex_pairs) / len(set(hex_pairs))] * len(set(hex_pairs))
    chi_stat, p_value = chisquare(observed, f_exp=expected)
    return chi_stat, p_value


# Calculate correlation between plaintext and ciphertext
def calculate_correlation_hex(plaintext, ciphertext_hex):
    plaintext_hex = plaintext.encode('utf-8').hex()
    plain_hex_pairs = [plaintext_hex[i:i+2] for i in range(0, len(plaintext_hex), 2)]
    cipher_hex_pairs = [ciphertext_hex[i:i+2] for i in range(0, len(ciphertext_hex), 2)]
    all_pairs = sorted(set(plain_hex_pairs) | set(cipher_hex_pairs))
    plain_freq = np.array([plain_hex_pairs.count(pair) for pair in all_pairs])
    cipher_freq = np.array([cipher_hex_pairs.count(pair) for pair in all_pairs])
    plain_freq = plain_freq / np.sum(plain_freq)
    cipher_freq = cipher_freq / np.sum(cipher_freq)
    correlation = np.corrcoef(plain_freq, cipher_freq)
    return correlation[0, 1]


def binary_to_hex(binary_string, without_0 = False):
    binary_string = binary_string.replace(" ", "")
    if without_0:
        binary_string = binary_string.replace("00000000", "")
    binary_string = binary_string.zfill(len(binary_string) + (4 - len(binary_string) % 4) % 4)
    hex_string = hex(int(binary_string, 2))[2:]
    return hex_string.zfill(len(binary_string) // 4)

# Function to run the tests and return average values
def run_tests(num_tests=100, show_plots=True, without_0 = True, save_file = True, Title = "test"):
    print(Title)
    entropy_values = []
    avalanche_values = []
    chi_stats = []
    p_values = []
    correlation_values = []
    key_sensitivity_avalanche_values = []  # List to store key sensitivity avalanche effect
    
    combined_frequency = {}  # Dictionary to store aggregated frequencies

    for _ in range(num_tests):
        plaintext = random_string(random.randint(100, 128))  # Random plaintext
        
        key = random_string(16)  # Random key of length 16
        alt_key = alternative_text(key, 5, 8)  # Alternative key

        ciphertext = remove_trailing_zeros(encrypt(plaintext, key))
        alt_ciphertext = remove_trailing_zeros(encrypt(plaintext, alt_key))

        ciphertext_hex = binary_to_hex(ciphertext, without_0)
        alt_ciphertext_hex = binary_to_hex(alt_ciphertext, without_0)

        # 1. Entropy calculation
        entropy = calculate_entropy_hex(ciphertext_hex)
        entropy_values.append(entropy)

        # 2. Avalanche effect calculation
        avalanche = avalanche_effect(ciphertext_hex, alt_ciphertext_hex)
        avalanche_values.append(avalanche)

        # 3. Chi-Square Test
        chi_stat, p_value = chi_square_test(ciphertext_hex)
        chi_stats.append(chi_stat)
        p_values.append(p_value)

        # 4. Plaintext-Ciphertext Correlation
        correlation = calculate_correlation_hex(plaintext, ciphertext_hex)
        correlation_values.append(correlation)

        # 5. Key Sensitivity Avalanche Effect
        key_diff_avalanche = avalanche_effect(ciphertext_hex, alt_ciphertext_hex)
        key_sensitivity_avalanche_values.append(key_diff_avalanche)
        
        # Frequency analysis
        freq = frequency_analysis(ciphertext_hex)
        for pair, count in freq.items():
            if pair in combined_frequency:
                combined_frequency[pair] += count
            else:
                combined_frequency[pair] = count

        print(f"Testing {_+1} out of {num_tests}", end="\r")

    # Normalize frequencies
    total_pairs = sum(combined_frequency.values())
    normalized_frequency = {pair: count / total_pairs for pair, count in combined_frequency.items()}
    

    # Plot combined frequency analysis
    if show_plots:
        plt.figure(figsize=(12, 6))
        plt.bar(normalized_frequency.keys(), normalized_frequency.values())
        plt.xlabel('Hex Pairs')
        plt.ylabel('Normalized Frequency')
        plt.title(f'Combined Frequency Analysis of Ciphertext (Hex Pairs) {Title}')
        plt.xticks(rotation=90)
        plt.tight_layout()
        # plt.show()
        if save_file:
            file_title = Title.replace(" ","_")
            file_title = file_title.replace("_-_", "-")
            file_path = f"frequency_analysis/{file_title}.png"
            plt.savefig(file_path)
            plt.close()
            
            csv_file = f"frequency_analysis/{file_title}.csv"
            with open(csv_file, mode='w', newline='') as csv_file:
                writer = csv.writer(csv_file)      
                writer.writerow(["Key", "Value"])
                for key, value in normalized_frequency.items():
                    writer.writerow([key, value])
        else:
            plt.show()


    # Calculate averages
    avg_entropy = np.mean(entropy_values)
    avg_avalanche = np.mean(avalanche_values)
    avg_chi_stat = np.mean(chi_stats)
    avg_p_value = np.mean(p_values)
    avg_correlation = np.mean(correlation_values)
    avg_key_sensitivity_avalanche = np.mean(key_sensitivity_avalanche_values)  # Average key sensitivity avalanche

    # Print averages
    print(f"\nAverage Entropy: {avg_entropy}")
    print(f"Average Avalanche Effect: {avg_avalanche}%")
    print(f"Average Chi-Square Statistic: {avg_chi_stat}")
    print(f"Average p-value: {avg_p_value}")
    print(f"Average Plaintext-Ciphertext Correlation: {avg_correlation}")
    print(f"Average Key Sensitivity Avalanche Effect: {avg_key_sensitivity_avalanche}%\n")


# Main function to run the tests
def main():
    run_tests(num_tests=100, show_plots=True)


if __name__ == "__main__":
    main()