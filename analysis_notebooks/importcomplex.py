import struct
import matplotlib.pyplot as plt
import numpy as np

# List of file names
file_names = ["./input_log_8mhz", "./output1_log_8mhz", "./output2_log_8mhz"]

# Create a new figure
plt.figure(figsize=(20, 10))

for i, file_name in enumerate(file_names, 1):
    with open(file_name, "rb") as file:
        data = file.read(10000000)

    # Number of complex numbers = total bytes / bytes per complex number
    num_complex_numbers = len(data) // 8
    floats = struct.unpack(f'<{2*num_complex_numbers}f', data)

    # Separate the real and imaginary parts
    real_parts = floats[::2]
    imaginary_parts = floats[1::2]

    real_parts = real_parts[999000:1000000]
    imaginary_parts = imaginary_parts[999000:1000000]

    # Create a subplot for each file and plot real and imaginary parts
    plt.subplot(len(file_names), 2, 2*i-1)
    plt.plot(real_parts, label='Real')
    plt.title(f'Real Parts from {file_name}')
    plt.xlabel('Index')
    plt.ylabel('Value')

    plt.subplot(len(file_names), 2, 2*i)
    plt.plot(imaginary_parts, label='Imaginary', color='red')
    plt.title(f'Imaginary Parts from {file_name}')
    plt.xlabel('Index')
    plt.ylabel('Value')

# Ensure a clean layout
plt.tight_layout()

# Display the plots
plt.show()
