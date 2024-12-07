import numpy as np
from math import log2
import matplotlib.pyplot as plt
from scipy.stats import chisquare

from process import encrypt, decrypt
from data import data_list
from utils import remove_trailing_zeros

# Function to calculate entropy
def calculate_entropy(text):
    frequency = {char: text.count(char) / len(text) for char in set(text)}
    entropy = -sum(p * log2(p) for p in frequency.values())
    return entropy


# Function for frequency analysis
def frequency_analysis(text):
    frequency = {char: text.count(char) for char in set(text)}
    return frequency


def plot_frequency(frequency):
    plt.bar(frequency.keys(), frequency.values())
    plt.xlabel('Characters')
    plt.ylabel('Frequency')
    plt.title('Frequency Analysis of Ciphertext')
    plt.show()


# Function to calculate Hamming distance between two strings
def hamming_distance(str1, str2):
    return sum(bin(ord(c1) ^ ord(c2)).count('1') for c1, c2 in zip(str1, str2))


# Function to calculate avalanche effect
def avalanche_effect(ciphertext1, ciphertext2):
    distance = hamming_distance(ciphertext1, ciphertext2)
    bit_difference = (distance / (len(ciphertext1) * 8)) * 100  # Percentage of differing bits
    return bit_difference


# Chi-square test for uniform distribution
def chi_square_test(text):
    observed = [text.count(char) for char in set(text)]
    expected = [len(text) / len(set(text))] * len(set(text))
    chi_stat, p_value = chisquare(observed, f_exp=expected)
    return chi_stat, p_value


# Function to calculate the correlation between plaintext and ciphertext
def calculate_correlation(plaintext, ciphertext):
    # Get the set of unique characters from both plaintext and ciphertext
    all_chars = sorted(set(plaintext) | set(ciphertext))
   
    # Calculate frequency of each character in both plaintext and ciphertext
    plain_freq = np.array([plaintext.count(char) for char in all_chars])
    cipher_freq = np.array([ciphertext.count(char) for char in all_chars])
   
    # Normalize the frequencies by dividing by the total count
    plain_freq = plain_freq / np.sum(plain_freq)
    cipher_freq = cipher_freq / np.sum(cipher_freq)
   
    # Calculate the correlation coefficient
    correlation = np.corrcoef(plain_freq, cipher_freq)
    return correlation[0, 1]


# Function to convert binary string to characters
def binary_to_text(binary_string):
    # Remove spaces from the binary string
    binary_string = binary_string.replace(" ", "")
   
    # Ensure the length of the binary string is a multiple of 8 (pad if necessary)
    if len(binary_string) % 8 != 0:
        raise ValueError("Binary string length should be a multiple of 8.")


    # Convert binary to text (decode in UTF-8)
    byte_array = bytearray(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
   
    try:
        return byte_array.decode('utf-8')
    except UnicodeDecodeError:
        return byte_array.decode('latin-1')  # If UTF-8 fails, try latin-1 for raw byte output


# Main function to accept inputs and calculate all metrics
def main():
    # Input plain text, key, ciphertext, and alternative key/ciphertext
    plaintext = input("Enter the plain text: ")
    
    key = input("Enter the encryption key: ")
    ciphertext = remove_trailing_zeros(encrypt(plaintext, key, data_list))
    ciphertext.replace("00000000","")

    
    alt_key = input("Enter the alternative encryption key: ")
    alt_ciphertext = remove_trailing_zeros(encrypt(plaintext, alt_key, data_list))
    alt_ciphertext.replace("00000000","")


    # Convert binary ciphertexts to text
    ciphertext = binary_to_text(ciphertext)
    alt_ciphertext = binary_to_text(alt_ciphertext)


    # 1. Entropy calculation
    entropy = calculate_entropy(ciphertext)
    print("Entropy of the ciphertext:", entropy)


    # 2. Frequency analysis and plotting
    freq = frequency_analysis(ciphertext)
    plt.figure()
    plot_frequency(freq)


    # 3. Avalanche effect testing
    avalanche = avalanche_effect(ciphertext, alt_ciphertext)
    print(f"Avalanche Effect: {avalanche:.2f}%")


    # 4. Chi-Square Test
    chi_stat, p_value = chi_square_test(ciphertext)
    print(f"Chi-Square Statistic: {chi_stat}, p-value: {p_value}")


    # 5. Plaintext-Ciphertext Correlation
    correlation = calculate_correlation(plaintext, ciphertext)
    print("Plaintext-Ciphertext Correlation:", correlation)


    # Plot correlation
    plt.figure()
    plt.bar([1, 2], [correlation, 1 - correlation], tick_label=["Correlation", "Complement"])
    plt.ylabel('Correlation Value')
    plt.title('Plaintext-Ciphertext Correlation')


    # 6. Key Sensitivity Test
    key_diff_avalanche = avalanche_effect(ciphertext, alt_ciphertext)
    print(f"Key Sensitivity Avalanche Effect: {key_diff_avalanche:.2f}%")


    # Plot key sensitivity
    plt.figure()
    plt.bar([1], [key_diff_avalanche])
    plt.ylabel('Avalanche Effect (%)')
    plt.title('Key Sensitivity Avalanche Effect')


    # Show all plots
    plt.show()


if __name__ == "__main__":
    main()
