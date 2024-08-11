#!/usr/bin/env python3
import sys
"""
Show some stats about a hex file, like number of occurances, spacing, and location.
Usage:
$ hxstat.py 11RungBlank "0D 04"
Number of occurrences: 11
Number of digits between occurrences:
Between occurrence 1 and 2: 102 digits
Between occurrence 2 and 3: 102 digits
Between occurrence 3 and 4: 102 digits
...
Occurrence 10: Byte 19287, Digit 38574
Occurrence 11: Byte 19338, Digit 38676

"""

def search_hex_in_file(file_path, hex_value):
    # Convert hex value to bytes
    hex_bytes = bytes.fromhex(hex_value)

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
            digits_between = (occurrences[i] - occurrences[i-1]) -1  # In bytes, -1 to not count the next instance
            print(f"Between occurrence {i} and {i+1}: {digits_between} bytes")
    
    print("Positions of occurrences:")
    for i, position in enumerate(occurrences, start=1):
        print(f"Occurrence {i}: Byte {position}, Digit {position+1}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file_path> <hex_value>")
        sys.exit(1)

    file_path = sys.argv[1]
    hex_value = sys.argv[2]
    search_hex_in_file(file_path, hex_value)

