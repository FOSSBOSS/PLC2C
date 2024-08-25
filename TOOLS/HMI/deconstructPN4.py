#!/usr/bin/env python3
"""
Done a lot of hacking this evening, hope this is the right file.
Decontruct .pn4 files into thier respective assets.

need to add a log or something. Resassemly has been a nightmare.

"""

import os
import sys
import gzip
import shutil

def decompress_file(compressed_file, output_dir):
    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)

    # Define the path for the decompressed file (temporary)
    decompressed_file = os.path.join(output_dir, 'temp.bin')
    
    # Decompress the file
    with gzip.open(compressed_file, 'rb') as f_in, open(decompressed_file, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    
    return decompressed_file

def extract_images_from_file(file_path, output_dir):
    with open(file_path, 'rb') as f:
        content = f.read()

    pos = 0
    while pos < len(content):
        # Look for the start of an image entry
        if b',WNV3/' in content[pos:]:
            entry_start = content.find(b',WNV3/', pos)
            if entry_start == -1:
                break

            # Find the end of the entry
            path_end = content.find(b',,', entry_start)
            if path_end == -1:
                break

            # Extract the file name (between ,WNV3/ and ,,)
            filename_start = entry_start + 1  # skip the comma before 'WNV3/'
            filename_end = path_end
            filename = content[filename_start:filename_end].decode('utf-8')
            filename = os.path.basename(filename)

            # Extract the number of bytes (after ,, and before newline)
            bytes_start = path_end + 2  # skip the ',,'
            bytes_end = content.find(b'\n', bytes_start)
            if bytes_end == -1:
                break

            try:
                num_bytes = int(content[bytes_start:bytes_end].decode('utf-8').strip())
            except ValueError:
                pos = bytes_end + 1
                continue

            # Extract the image data
            image_data_start = bytes_end + 1
            image_data_end = image_data_start + num_bytes
            if image_data_end > len(content):
                break

            image_data = content[image_data_start:image_data_end]

            # Save the image to the output directory
            output_path = os.path.join(output_dir, filename)
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'wb') as img_file:
                img_file.write(image_data)
            print(f"Extracted: {output_path}")

            # Move the position past the current image data
            pos = image_data_end
        else:
            break

def main():
    if len(sys.argv) != 2:
        print("Usage: python extract_images.py <file.pn4>")
        sys.exit(1)

    pn4_file = sys.argv[1]
    if not os.path.isfile(pn4_file):
        print(f"File not found: {pn4_file}")
        sys.exit(1)

    # Create output directory based on the pn4 file name
    base_name = os.path.splitext(os.path.basename(pn4_file))[0]
    output_dir = os.path.join(os.getcwd(), base_name)

    # Decompress the file into the output directory
    decompressed_file = decompress_file(pn4_file, output_dir)

    # Extract images from the decompressed file
    extract_images_from_file(decompressed_file, output_dir)

    # Optionally, remove the temporary decompressed file
    os.remove(decompressed_file)

if __name__ == "__main__":
    main()
