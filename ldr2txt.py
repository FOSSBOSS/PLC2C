#!/usr/bin/env python3
"""
Usage:
$ldr2txt.py projectName.ldr
(this program takes a ldr file from the output of deconstuctPJW.py)
Make dealing with the binary segments of the decompressed project datafile simpler,
by converting them to text, maintainging text characters as text, 
and converting control, hidden, and formating characters to thier 
respective string litteral. 
The motivation here was on how to edit program space after realizing 
the entire executable segment of the WindLDR project is on a single 
line, and that string manipulation is easier than binary manipulation.

This is a temp program, its functionality will be integrated into plc2c.py 
at a later date. I still have to figure out what I want to do with the 
Character^@ array present in the same subsection. I'm thinking, parse it out, 
and turn it into a config file. 
"""
import sys
import os

def process_ldr_file(ldr_file):
    output_file = ldr_file + '.txt'
    
    try:
        with open(ldr_file, 'rb') as f_in, open(output_file, 'w') as f_out:
            byte = f_in.read(1)
            while byte:
                hex_value = byte.hex().upper()
                int_value = int(hex_value, 16)
                if hex_value == '0A':
                    f_out.write('\n0A')       # might want start / end new lines here. 
                elif 32 <= int_value <= 126:  # ASCII printable range
                    f_out.write(chr(int_value))
                else:
                    f_out.write(hex_value)
                byte = f_in.read(1)
    except Exception as e:
        print(f"Error processing file {ldr_file}: {e}")

def main():
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename.ldr>")
        sys.exit(1)

    ldr_file = sys.argv[1]
    if not os.path.isfile(ldr_file) or not ldr_file.endswith('.ldr'):
        print(f"Invalid file: {ldr_file}")
        sys.exit(1)

    process_ldr_file(ldr_file)

if __name__ == "__main__":
    main()
