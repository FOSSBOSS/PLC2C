#!/usr/bin/env python3
"""
buggy.
it might be the only way to  reconstruct a pn4 is to know how it was built in the first place. 

This program attempts to reconstitute a deconstructed  pn4 file.

"""

import os
import sys
import gzip
import shutil

def rebuild_pn4(folder_path, original_pn4_name):
    rebuilt_folder = "rebuilt"
    os.makedirs(rebuilt_folder, exist_ok=True)

    output_bin_path = os.path.join(rebuilt_folder, original_pn4_name.replace(".pn4", ".bin"))
    output_pn4_path = os.path.join(rebuilt_folder, original_pn4_name)

    step_number = 0
    with open(output_bin_path, 'wb') as bin_file:
        files_in_folder = os.listdir(folder_path)

        # Step 1: Add .bin files in alphabetical order
        for file_name in sorted(f for f in files_in_folder if f.endswith('.bin')):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'rb') as file_data:
                file_bytes = file_data.read()

            entry_header = f"{step_number},SIMULATOR/DEVICEVALUE/{file_name},,{len(file_bytes)}\n".encode('utf-8')
            bin_file.write(entry_header)
            bin_file.write(file_bytes)
            step_number += 1

        # Step 2: Add bsNNNN.o2f files in sequence
        for file_name in sorted(f for f in files_in_folder if f.startswith('bs') and f.endswith('.o2f')):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'rb') as file_data:
                file_bytes = file_data.read()

            entry_header = f"{step_number},WNV3/{file_name},,{len(file_bytes)}\n".encode('utf-8')
            bin_file.write(entry_header)
            bin_file.write(file_bytes)
            step_number += 1

        # Step 3: Add External DeviceN.tag files
        for file_name in sorted(f for f in files_in_folder if f.endswith('.tag')):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'rb') as file_data:
                file_bytes = file_data.read()

            entry_header = f"{step_number},WNV3/{file_name},,{len(file_bytes)}\n".encode('utf-8')
            bin_file.write(entry_header)
            bin_file.write(file_bytes)
            step_number += 1

        # Step 4: Add .png files
        for file_name in sorted(f for f in files_in_folder if f.endswith('.png')):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'rb') as file_data:
                file_bytes = file_data.read()

            entry_header = f"{step_number},WNV3/WEBPAGE/viewer/setting/{file_name},,{len(file_bytes)}\n".encode('utf-8')
            bin_file.write(entry_header)
            bin_file.write(file_bytes)
            bin_file.write(b'\n')  # Ensure newline after each .png file
            step_number += 1

        # Step 5: Add def_video.mp4
        def_video_path = os.path.join(folder_path, 'def_video.mp4')
        if os.path.exists(def_video_path):
            with open(def_video_path, 'rb') as file_data:
                file_bytes = file_data.read()

            entry_header = f"{step_number},WNV3/WEBPAGE/viewer/setting/def_video.mp4,,{len(file_bytes)}\n".encode('utf-8')
            bin_file.write(entry_header)
            bin_file.write(file_bytes)
        else:
            print("Warning: def_video.mp4 not found.")

    # Compress the binary file to a .pn4 file
    with open(output_bin_path, 'rb') as bin_file, gzip.open(output_pn4_path, 'wb') as pn4_file:
        shutil.copyfileobj(bin_file, pn4_file)

    print(f"Reassembled file: {output_pn4_path}")

    # Check for files not included
    included_files = {f for f in files_in_folder if f.endswith(('.bin', '.o2f', '.tag', '.png', '.mp4'))}
    excluded_files = set(files_in_folder) - included_files
    if excluded_files:
        print("Files not included in the rebuilt .pn4 file:", excluded_files)

def main():
    if len(sys.argv) != 3:
        print("Usage: python rebuild_pn4.py <folder_with_extracted_files> <original_pn4_name>")
        sys.exit(1)

    folder_with_extracted_files = sys.argv[1]
    original_pn4_name = sys.argv[2]

    if not os.path.isdir(folder_with_extracted_files):
        print(f"Folder not found: {folder_with_extracted_files}")
        sys.exit(1)

    rebuild_pn4(folder_with_extracted_files, original_pn4_name)

if __name__ == "__main__":
    main()
