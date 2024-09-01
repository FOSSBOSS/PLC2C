#!/usr/bin/env python3
import sys
import binascii
import os

def convert_to_bytes(input_str):
    try:
        # Attempt to interpret input as a hex value
        return bytes.fromhex(input_str)
    except ValueError:
        # If that fails, treat it as a regular string and convert to bytes
        return input_str.encode('utf-8')

def search_hex_or_string_in_file(file_path, start_pattern, end_pattern=None):
    # Convert patterns to bytes
    start_bytes = convert_to_bytes(start_pattern)
    start_byte_length = len(start_bytes)

    if end_pattern:
        end_bytes = convert_to_bytes(end_pattern)
    else:
        end_bytes = None

    # Read the binary file
    with open(file_path, 'rb') as file:
        content = file.read()

    # Find all occurrences of the start pattern in the file
    occurrences = []
    start = 0
    while True:
        start = content.find(start_bytes, start)
        if start == -1:
            break
        occurrences.append(start)
        start += len(start_bytes)

    # Print results
    num_occurrences = len(occurrences)
    print(f"Number of occurrences: {num_occurrences}")

    if end_bytes:
        # Search between occurrences of start_pattern and end_pattern
        print("Occurrences between start and end patterns:")
        for i in range(num_occurrences):
            end_position = content.find(end_bytes, occurrences[i] + len(start_bytes))
            if end_position != -1:
                length_between = end_position - (occurrences[i] + len(start_bytes))
                print(f"Start: {occurrences[i]} End: {end_position} Length: {length_between} bytes")
            else:
                print(f"Start pattern found at {occurrences[i]}, but no end pattern found.")

    if num_occurrences > 1:
        print("Number of bytes between occurrences:")
        for i in range(1, num_occurrences):
            bytes_between = (occurrences[i] - occurrences[i-1]) - start_byte_length   # Account for the search argument length
            print(f"Between occurrence {i} and {i+1}: {bytes_between} bytes")
    
    print("Positions of occurrences:")
    for i, position in enumerate(occurrences, start=1):
        # Output the byte position and number of bytes that the search argument represents
        print(f"Occurrence {i}: Start Byte {position}, Span {start_byte_length} bytes")

if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(f"Usage: {os.path.basename(sys.argv[0])} <file_path> \"hex or string\"\n OR:")
        print(f"Usage: {os.path.basename(sys.argv[0])} <file_path> \"hex or string\" \"hex or string\" \nOR:\n")
      

        sys.exit(1)

    file_path = sys.argv[1]
    start_pattern = sys.argv[2]
    end_pattern = sys.argv[3] if len(sys.argv) == 4 else None

    search_hex_or_string_in_file(file_path, start_pattern, end_pattern)

"""
Dev version0.1
./hxstat.py <file_name> <hex_value>
added option:
./hxstat.py <file_name> <hex_value> <hex_value_end>

Future Feature ideas:
Wildcard support
case insensitive search
highlight patterns in output
Define actual statistical analysis: std dev, mean, mode, median...
do a count instead of listing every thing, or clean output.
Interactive mode?
Live edit?
ML LOL. ... but for real, supposing I could implement it, the pattern analysis could be awesome.
CLI flags. 

"""
