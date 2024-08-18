#!/usr/bin/env python3
import sys
"""
This program is for searching patterns in binaries.
"""
def search_hex_in_file(file_path, hex_value):
    # Convert hex value to bytes
    hex_bytes = bytes.fromhex(hex_value)
    hex_byte_length = len(hex_bytes)  # Calculate the number of bytes in the search argument

    # Read the binary file
    with open(file_path, 'rb') as file:
        content = file.read()

    # Find all occurrences of the hex value in the file
    occurrences = []
    start = 0
    while True:
        start = content.find(hex_bytes, start)
        if start == -1:
            break
        occurrences.append(start)
        start += len(hex_bytes)

    # Print results
    num_occurrences = len(occurrences)
    print(f"Number of occurrences: {num_occurrences}")
    
    if num_occurrences > 1:
        print("Number of digits between occurrences:")
        for i in range(1, num_occurrences):
            digits_between = (occurrences[i] - occurrences[i-1]) - hex_byte_length   # Account for the search argument length
            print(f"Between occurrence {i} and {i+1}: {digits_between} bytes")
    
    print("Positions of occurrences:")
    for i, position in enumerate(occurrences, start=1):
        # Output the byte position and number of bytes that the hex argument represents
        print(f"Occurrence {i}: Start Byte {position}, Span {hex_byte_length} bytes")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file_path> <hex_value>")
        sys.exit(1)

    file_path = sys.argv[1]
    hex_value = sys.argv[2]
    search_hex_in_file(file_path, hex_value)
