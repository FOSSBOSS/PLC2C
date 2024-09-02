#!/usr/bin/env python3
import os
import sys
import struct

def load_ladder_file(file_path):
    """Load the binary content of the ladder logic file."""
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        sys.exit(1)

def find_program_space(content, start_marker, end_marker):
    """Locate the program space within the content using start and end markers."""
    start_pos = content.find(start_marker)
    if start_pos == -1:
        print("Start marker not found.")
        sys.exit(1)
    end_pos = content.find(end_marker, start_pos)
    if end_pos == -1:
        print("End marker not found.")
        sys.exit(1)
    end_pos += len(end_marker)  # Include end marker in the program space
    return content[start_pos:end_pos], start_pos

def find_lcal_occurrences(program_space):
    """Find all occurrences of 'LCAL' in the program space."""
    sequence = b'LCAL'
    positions = []
    start = 0
    while True:
        pos = program_space.find(sequence, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + len(sequence)
    return positions

def extract_context(program_space, positions, context_size=16):
    """Extract bytes surrounding each 'LCAL' occurrence."""
    contexts = []
    for idx, pos in enumerate(positions):
        start = max(pos - context_size, 0)
        end = pos + len(b'LCAL') + context_size
        snippet = program_space[start:end]
        contexts.append({
            'index': idx + 1,
            'position': pos,
            'context_hex': ' '.join(f'{byte:02X}' for byte in snippet),
            'context_ascii': ''.join((chr(byte) if 32 <= byte <= 126 else '.') for byte in snippet)
        })
    return contexts

def print_contexts(contexts):
    """Print the extracted contexts in a readable format."""
    for context in contexts:
        print(f"Occurrence {context['index']}:")
        print(f"Position (offset): {context['position']}")
        print(f"Context (Hex): {context['context_hex']}")
        print(f"Context (ASCII): {context['context_ascii']}")
        print("-" * 60)

def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_lcal.py <ladder_file_path>")
        sys.exit(1)

    ladder_file_path = sys.argv[1]
    if not os.path.isfile(ladder_file_path):
        print(f"File not found: {ladder_file_path}")
        sys.exit(1)

    # Load ladder file content
    content = load_ladder_file(ladder_file_path)

    # Define start and end markers
    start_marker = bytes.fromhex('23 00 00 00 39')
    end_marker = bytes.fromhex('01 00 01 00 00 00 00 FF 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00 0A')

    # Find program space
    program_space, program_offset = find_program_space(content, start_marker, end_marker)

    # Find 'LCAL' occurrences
    lcal_positions = find_lcal_occurrences(program_space)

    if not lcal_positions:
        print("No occurrences of 'LCAL' found in program space.")
        sys.exit(0)

    # Extract contexts around 'LCAL'
    contexts = extract_context(program_space, lcal_positions, context_size=16)

    # Print contexts
    print_contexts(contexts)

if __name__ == "__main__":
    main()
