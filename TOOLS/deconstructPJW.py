#!/usr/bin/env python3
"""
Deconstruct the input project file, and extract the extended features characters to:
basename_ExtendedCharacters.txt
might opt to remove these lines from the ldr source file. havent decided yet.
"""

import os
import sys
import shutil
import gzip
import logging
from datetime import datetime

def setup_logging():
    user = os.getenv('USER')
    log_dir = f'/home/{user}/bin'
    log_file = os.path.join(log_dir, 'plc2c.log')
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

def log_message(message):
    logging.info(message)
    print(message)

def hex_to_ascii(hex_str):
    return bytes.fromhex(hex_str).decode('ascii', errors='ignore')

def process_ldr_file(ldr_file, sub_dir):
    output_file = os.path.join(sub_dir, os.path.splitext(ldr_file)[0] + '_ExtendedCharacters.txt')
    
    try:
        with open(ldr_file, 'rb') as f_in, open(output_file, 'w') as f_out:
            content = f_in.read()
            hex_chars = "43686172616374657273"
            start = 0
            while start < len(content):
                index = content.find(bytes.fromhex(hex_chars), start)
                if index == -1:
                    break
                end = content.find(b'\x0A', index + 1)
                if end == -1:
                    end = len(content)
                line = content[index + len(bytes.fromhex(hex_chars)):end].hex().upper()
                f_out.write("Characters\n")
                f_out.write(f"{line}\n")
                start = end + 1
    except Exception as e:
        log_message(f"Error processing LDR file {ldr_file}: {e}")

def process_pjw_file(pjw_file):
    basename = os.path.splitext(pjw_file)[0]
    sub_dir = os.path.join(os.getcwd(), basename)
    
    if os.path.exists(sub_dir):
        log_message("File exists")
        return

    os.makedirs(sub_dir, exist_ok=True)
    new_file = os.path.join(sub_dir, basename + '.gz')
    shutil.copyfile(pjw_file, new_file)

    try:
        with gzip.open(new_file, 'rb') as f_in:
            extracted_file = os.path.join(sub_dir, basename + '.ldr')
            with open(extracted_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except Exception as e:
        log_message(f"Error extracting {new_file}: {e}")
        return
    
    try:
        with open(extracted_file, 'rb') as f:
            content = f.read()
            lines = content.split(b'\n')
            for line in lines:
                parts = line.split(b',')
                if len(parts) >= 4:
                    number, filename1, filename2, bytes_field = parts[:4]
                    number = number.decode()
                    filename1 = filename1.decode()
                    filename2 = filename2.decode()
                    bytes_field = bytes_field.decode()
                    
                    if filename1 and basename not in filename1:
                        log_message(f"Filename mismatch: {filename1}")
                    elif filename2 and basename not in filename2:
                        log_message(f"Filename mismatch: {filename2}")
                    output_filename = filename1 or filename2
                    output_filepath = os.path.join(sub_dir, output_filename)
                    if b'.tag' in output_filename.encode():
                        output_filepath = output_filepath.replace('.tag', '.xml')
                    try:
                        bytes_to_read = int(bytes_field)
                        start_index = content.index(line) + len(line) + 1  # +1 to skip the newline character
                        file_content = content[start_index:start_index + bytes_to_read]
                        with open(output_filepath, 'wb') as f_out:
                            f_out.write(file_content)
                    except ValueError:
                        log_message(f"Invalid bytes field: {bytes_field}")
                    except Exception as e:
                        log_message(f"Error writing to file {output_filepath}: {e}")
    except Exception as e:
        log_message(f"Error processing extracted file {extracted_file}: {e}")
    
    process_ldr_file(extracted_file, sub_dir)

def main():
    setup_logging()

    if len(sys.argv) != 2:
        log_message("Usage: python plc2c.py <filename.pjw>")
        sys.exit(1)

    pjw_file = sys.argv[1]
    if not os.path.isfile(pjw_file) or not pjw_file.endswith('.pjw'):
        log_message(f"Invalid file: {pjw_file}")
        sys.exit(1)

    process_pjw_file(pjw_file)

if __name__ == "__main__":
    main()
