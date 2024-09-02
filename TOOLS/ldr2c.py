#!/usr/bin/env python3
import os
"""
OK, this is no where near done, but Im tired AF.
binary analyis didnt give me much beyond the basic structures already listed in
https://github.com/FOSSBOSS/PLC2C/blob/main/DOCUMENTATION/Initial.txt

however, 03 0A might be an end of rung new line. I have to make some test files for that.

Eh... 
on page 482 of the idec microsmart user manual, there are a list of basic instructions, 
which this code is attempting to generate C code on the basis of. 
It can not possibly work as is, but the purpose ( intent ) of 
this program is to generate C code from the extracted *.ldr component of a PJW file.

you can generate a *.ldr file by using deconstructPJW.py against a PJW file.
dev_ version is sorta better RN, but I found a bug I have to fix.
(BYTES) write to the successive code extensions.

anyway, Ill also have to add a function to accept the other program code files,
such as .sub, and .cmt. .. and what ever relivent files may also exist. 

I'll add more instructions later

"""

def parse_ldr_file(ldr_file_path):
    with open(ldr_file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data

def interpret_byte_sequence(byte_seq):
    # Example mapping from byte sequences to C operations
    # Add more mappings as needed
    mapping = {
        b'\x0B\x04': 'vertical_line();',
        b'\x0D\x04': 'add_rung();',
        b'\xF8\x03': 'horizontal_line();',
        b'\xE9\x03': 'AND(',    # Assume it needs a closing ')'
        b'\xEA\x03': 'OR(',     # Assume it needs a closing ')'
        b'\xEB\x03': 'SET(',    # Assume it needs a closing ')'
        b'\xEC\x03': 'SOTD(',   # Assume it needs a closing ')'
        b'\xEF\x03': 'SOTU(',   # Assume it needs a closing ')'
        b'\xF0\x03': 'RST(',    # Assume it needs a closing ')'
        b'\x4C\x43\x41\x4C': 'LCAL_OPERATION();',
        # Add more mappings here based on known structures
    }
    return mapping.get(byte_seq, '// Unknown operation')

def generate_c_code(binary_data):
    c_code_lines = []
    i = 0
    while i < len(binary_data):
        # Look for known byte sequences and interpret them
        byte_seq = binary_data[i:i+2]  # Considering 2-byte sequences for simplicity
        c_code_line = interpret_byte_sequence(byte_seq)
        c_code_lines.append(c_code_line)
        i += 2  # Move to the next byte sequence

    return '\n'.join(c_code_lines)

def write_c_file(c_code, output_file_path):
    with open(output_file_path, 'w') as c_file:
        c_file.write('#include <stdio.h>\n\n')
        c_file.write('void vertical_line() { /* Implement logic */ }\n')
        c_file.write('void add_rung() { /* Implement logic */ }\n')
        c_file.write('void horizontal_line() { /* Implement logic */ }\n')
        c_file.write('void AND(int x, int y) { /* Implement logic */ }\n')
        c_file.write('void OR(int x, int y) { /* Implement logic */ }\n')
        c_file.write('void SET(int *x) { *x = 1; }\n')
        c_file.write('void SOTD(int *x) { *x = 0; }\n')
        c_file.write('void SOTU(int *x) { *x = 1; }\n')
        c_file.write('void RST(int *x) { *x = 0; }\n')
        c_file.write('void LCAL_OPERATION() { /* Implement LCAL logic */ }\n')
        c_file.write('\n')
        c_file.write('int main() {\n')
        c_file.write(c_code)
        c_file.write('\n    return 0;\n')
        c_file.write('}\n')

def main():
    ldr_file_path = 'Project1.ldr'          # Make this basename function of input arg
    output_file_path = 'generated_program.c'
    
    binary_data = parse_ldr_file(ldr_file_path)
    c_code = generate_c_code(binary_data)
    write_c_file(c_code, output_file_path)
    
    print(f'C source code generated and saved to {output_file_path}')

if __name__ == "__main__":
    main()
