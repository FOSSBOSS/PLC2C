#!/usr/bin/env python3
import os
import sys
import shutil
import gzip
import logging
from datetime import datetime
"""
Updated file extensions, how sections with directories are handled, ( we make folders now )
Is there error handling? lol not really.
Are there errors? oh yeah! Heres some:
$dev_deconstructPJW.py Project.pjw  | grep -i Invalid
Invalid bytes field: b']\x01\r>\\\x01\r*]\x15\r\x00\x00\x02\r4]\x01\rj\x80\x1e\rZ\x00\x01\r4]\x01\r'
Invalid bytes field: b'C\xbe\xdf'
Invalid bytes field: b'"Remote_Enable"'
Invalid bytes field: b'\x00\x03\x00Dp\x01\x00\xa3\\\xb5_\xa3\\\x00\x00B\x00\x01\x00V\x04\x00\x00'
Invalid bytes field: b' compressor'
Invalid bytes field: b'"Remote_Enable"'
Invalid bytes field: b' \r'
Invalid bytes field: b' the start up routine could start the valve process and the cond and evap flow stuff but then get stuck at the llsv. so instead'
Invalid bytes field: b'\x00\x05\x00\x00\x00M0020\xf4\x03\x00\x00\x01\x00'
Invalid bytes field: b' the config bit would be reverted\r'
Invalid bytes field: b'\x00\xf8\x03\x00\x00\x07\x00'
Invalid bytes field: b'\x00\x0c\x00'
Invalid bytes field: b' unit  purging. \r'
Invalid bytes field: b' unit has finished.\r'
Invalid bytes field: b' or post purging. \r'
Invalid bytes field: b' or post purge is active and PID start is OFF. \r'
Invalid bytes field: b' prject specific comentary omited. !!\r'
Invalid bytes field: b' and llsv'

\r seems like a common choking point here. 
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
                parts = line.split(b',')
                if len(parts) >= 4:
                    number, filename, _, bytes_field = parts[:4]
                    try:
                        bytes_to_read = int(bytes_field)
                    except ValueError:
                        log_message(f"Invalid bytes field: {bytes_field}")
                        continue
                    
                    filename = filename.decode('utf-8', errors='ignore').strip()
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
