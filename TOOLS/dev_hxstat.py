#!/usr/bin/env python3
import sys
import os
"""
ima break this one. its working now, but Ima break it real soon with dev bs.

"""
def search_hex_in_file(file_path, hex_value, hex_value_end=None):
    # Convert hex values to bytes
    hex_bytes = bytes.fromhex(hex_value)
    hex_byte_length = len(hex_bytes)  # Calculate the number of bytes in the search argument

    if hex_value_end:
        hex_bytes_end = bytes.fromhex(hex_value_end)
    else:
        hex_bytes_end = None

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

    if hex_bytes_end:
        # Search between occurrences of hex_value and hex_value_end
        print("Occurrences between start and end patterns:")
        for i in range(num_occurrences):
            end_position = content.find(hex_bytes_end, occurrences[i] + len(hex_bytes))
            if end_position != -1:
                length_between = end_position - (occurrences[i] + len(hex_bytes))
                print(f"Start: {occurrences[i]} End: {end_position} Length: {length_between} bytes")
            else:
                print(f"Start pattern found at {occurrences[i]}, but no end pattern found.")

    if num_occurrences > 1:
        print("Number of bytes between occurrences:")
        for i in range(1, num_occurrences):
            bytes_between = (occurrences[i] - occurrences[i-1]) - hex_byte_length   # Account for the search argument length
            print(f"Between occurrence {i} and {i+1}: {bytes_between} bytes")
    
    print("Positions of occurrences:")
    for i, position in enumerate(occurrences, start=1):
        # Output the byte position and number of bytes that the hex argument represents
        print(f"Occurrence {i}: Start Byte {position}, Span {hex_byte_length} bytes")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(f"Usage: {os.path.basename(sys.argv[0])} <file_path> \"hex_value\"\n OR:")
        print(f"Usage: {os.path.basename(sys.argv[0])} <file_path> \"hex_value\" \"hex_value_end\"")
        sys.exit(1)

    file_path = sys.argv[1]
    hex_value = sys.argv[2]
    hex_value_end = sys.argv[3] if len(sys.argv) == 4 else None

    search_hex_in_file(file_path, hex_value, hex_value_end)



"""
Dev version0.1
./hxstat.py <file_name> <hex_value>
added option:
./hxstat.py <file_name> <hex_value> <hex_value_end>

"""
