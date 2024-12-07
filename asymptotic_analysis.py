from process import encrypt, decrypt

import time
import random
import string

import numpy as np
import matplotlib.pyplot as plt
import csv
from numpy.polynomial.polynomial import Polynomial

key = "nUv2pkXTvBbJevEWitititjghfyrnghvuf"

# Example encryption and decryption functions (you can replace these with your actual functions)
def encrypt_test(plaintext):
    return encrypt(plaintext, key)
    
def decrypt_test(ciphertext):
    return decrypt(ciphertext, key)
    
def test_speed():
    # List to store results
    lengths = []
    encryption_times = []
    decryption_times = []

    # Test with increasing lengths of plaintext
    for length in range(1, 220):  # Change the range as needed
        plaintext = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
        
        # Measure encryption time
        start_time = time.time()
        encrypted_text = encrypt_test(plaintext)
        encryption_time = time.time() - start_time

        # Measure decryption time
        start_time = time.time()
        decrypted_text = decrypt_test(encrypted_text)
        decryption_time = time.time() - start_time
        
        # Store the results
        lengths.append(length)
        encryption_times.append(encryption_time)
        decryption_times.append(decryption_time)
        
        print(f"Length: {length}, Encryption Time: {encryption_time:.6f}s, Decryption Time: {decryption_time:.6f}s")
    
    return lengths, encryption_times, decryption_times

# Run the speed test
lengths, encryption_times, decryption_times = test_speed()

# Polynomial Regression for Smoothing
def smooth_curve(x, y, degree=5):
    coefs = Polynomial.fit(x, y, degree)  # Fit a polynomial of the given degree
    smooth_x = np.linspace(min(x), max(x), 500)  # Generate evenly spaced x-values
    smooth_y = coefs(smooth_x)  # Compute the smoothed y-values
    return smooth_x, smooth_y

# Apply smoothing for both encryption and decryption times
degree = 5  # Adjust the degree of the polynomial for desired smoothness
smoothed_lengths_enc, smoothed_encryption_times = smooth_curve(lengths, encryption_times, degree)
smoothed_lengths_dec, smoothed_decryption_times = smooth_curve(lengths, decryption_times, degree)

# Plotting the results
plt.figure(figsize=(12, 6))

# Original data
plt.plot(lengths, encryption_times, label="Original Encryption Time", linestyle='--', color='blue', alpha=0.6)
plt.plot(lengths, decryption_times, label="Original Decryption Time", linestyle='--', color='orange', alpha=0.6)

# Smoothed data
plt.plot(smoothed_lengths_enc, smoothed_encryption_times, label="Smoothed Encryption Time", color='blue')
plt.plot(smoothed_lengths_dec, smoothed_decryption_times, label="Smoothed Decryption Time", color='orange')

plt.xlabel("Plaintext Length")
plt.ylabel("Time (seconds)")
plt.title("Encryption and Decryption Speed Test (Original vs Smoothed)")
plt.legend()
plt.grid(True)
plt.show()

# Save results to a CSV file for further analysis
with open('encryption_decryption_speeds.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Plaintext Length", "Encryption Time", "Decryption Time"])
    for i in range(len(lengths)):
        writer.writerow([lengths[i], encryption_times[i], decryption_times[i]])

print("Results saved to encryption_decryption_speeds.csv")
