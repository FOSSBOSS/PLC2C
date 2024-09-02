#!/usr/bin/env python3
import os
import sys
import shutil
import gzip
import logging
from datetime import datetime
"""
Not throughtly tested.
sanitized !! and \r occurances.
Need to verify that the files are intact.... 

ok, one issue is some of the bytes, from the bytes section make it into file output.  which is a no no.
"""


# Define text and binary extensions
TEXT_EXTENSIONS = {'.ini', '.tag', '.xml'}
BINARY_EXTENSIONS = {'.bmk', '.cod', '.cmt', '.cus', '.ldr', '.pcv', '.obu', '.sip', '.sub', '.sym'}

def setup_logging(basename):
    log_dir = os.path.join(os.getcwd(), basename)
    log_file = os.path.join(log_dir, f'deconstructed_{basename}.log')
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(message)s')

def log_message(message):
    logging.info(message)
    print(message)

def sanitize_line(line):
    # Remove any unexpected characters
    line = line.replace(b'\r', b'').replace(b'!!', b'')
    return line

def is_valid_bytes_field(bytes_field):
    try:
        # Check if bytes_field can be cast to an integer
        int(bytes_field)
        return True
    except ValueError:
        return False

def write_section(output_filepath, content, is_text):
    mode = 'w' if is_text else 'wb'
    with open(output_filepath, mode) as f_out:
        if is_text:
            f_out.write(content.decode('utf-8', errors='ignore'))
        else:
            f_out.write(content)

def process_pjw_file(pjw_file):
    basename = os.path.splitext(pjw_file)[0]
    sub_dir = os.path.join(os.getcwd(), basename)
    
    if os.path.exists(sub_dir):
        log_message("File exists")
        return

    os.makedirs(sub_dir, exist_ok=True)
    setup_logging(basename)

    new_file = os.path.join(sub_dir, basename + '.gz')
    shutil.copyfile(pjw_file, new_file)

    try:
        with gzip.open(new_file, 'rb') as f_in:
            extracted_file = os.path.join(sub_dir, basename + '.bin')
            with open(extracted_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
    except Exception as e:
        log_message(f"Error extracting {new_file}: {e}")
        return
    
    try:
        with open(extracted_file, 'rb') as f:
            content = f.read()
            lines = content.split(b'\n')
            offset = 0

            for line in lines:
                line = sanitize_line(line)  # Clean the line before processing
                parts = line.split(b',')
                if len(parts) >= 4:
                    number = parts[0].decode('utf-8', errors='ignore').strip()
                    filename = parts[1].decode('utf-8', errors='ignore').strip()
                    bytes_field = parts[3].decode('utf-8', errors='ignore').strip()
                    
                    if not is_valid_bytes_field(bytes_field):
                        log_message(f"Invalid bytes field: {parts[3]}. Skipping this section.")
                        continue
                    
                    bytes_to_read = int(bytes_field)
                    
                    if not filename:
                        continue
                    
                    section_data = content[offset + len(line) + 1 : offset + len(line) + 1 + bytes_to_read]
                    
                    # Log the section
                    log_message(line.decode('utf-8', errors='ignore'))
                    
                    # Determine if the filename includes a subdirectory
                    if '/' in filename:
                        subdirectory = os.path.join(sub_dir, os.path.dirname(filename))
                        os.makedirs(subdirectory, exist_ok=True)
                    else:
                        subdirectory = sub_dir

                    output_filepath = os.path.join(subdirectory, os.path.basename(filename))
                    
                    # Check extension and write the file accordingly
                    extension = os.path.splitext(filename)[1].lower()
                    if extension in TEXT_EXTENSIONS:
                        write_section(output_filepath, section_data, is_text=True)
                    elif extension in BINARY_EXTENSIONS:
                        write_section(output_filepath, section_data, is_text=False)
                    else:
                        log_message(f"Unrecognized extension {extension}. Skipping this section.")
                        continue
                    
                    # Update the offset for the next section
                    offset += len(line) + 1 + bytes_to_read

    except Exception as e:
        log_message(f"Error processing extracted file {extracted_file}: {e}")

def main():
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



"""
Deconstruct the input project file, and extract the extended features characters to:
basename_ExtendedCharacters.txt
might opt to remove these lines from the ldr source file. havent decided yet.

Deconstruct PJW files using the following tags:
Text Extensions, then Binary Extensions:
.ini 
.tag
.xml

.bmk 
.cod 
.cmt 
.cus 
.ldr
.pcv
.obu
.sip
.sub 
.sym 

FMI See: https://github.com/FOSSBOSS/PLC2C/blob/main/DOCUMENTATION/PJW_PARTS.txt
"""
