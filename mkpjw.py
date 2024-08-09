#!/usr/bin/env python3
"""
ok some minor issues left, but I tire.
re rxtracting the dat file from the compressed file pjw
results in a file with the pjw extension. 
Which is confusing. maybe name it basename, or basename.dat
something that can not be confussed for another file which may
exist. 

output to basename.dat is handy for debugging, ..
"""

import os
import sys
import gzip

def read_file(file_path):
    """Read the contents of a file if it exists."""
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'rb') as f:
        return f.read()

def write_entry(output, count, file_name, content):
    """Write an entry for a file to the output."""
    if content is not None:
        output.write(f"{count},{file_name},,{len(content)}\n".encode('ascii'))
        output.write(content)
        output.write(b"\n")  # Add a newline after the file content

def main(basename, compress=False):
    files_to_process = [
        "CommentDownloadSettings.ini",
        f"{basename}.bmk",
        f"{basename}.cmt",
        f"{basename}.cod",
        f"{basename}.ldr",
        f"{basename}.obu",
    ]

    count = 0
    output_file = f"{basename}.pjw" if compress else f"{basename}.dat"

    with (gzip.open(output_file, 'wb') if compress else open(output_file, 'wb')) as output:
        for file_name in files_to_process:
            content = read_file(file_name)

            if file_name.endswith(".ldr") and content is None:
                print("No ladder found, program cannot possibly complete.")
                return

            if content is None:
                print(f"Warning: {file_name} not found.")
                continue

            write_entry(output, count, file_name, content)

            #if file_name.endswith(".bmk"):
            #    output.write(b"\x00\x00\n")  
            count += 1

        xml_file = f"{basename}.xml"
        xml_pcv_file = f"{basename}_PCV.xml"

        if os.path.exists(xml_file):
            output.write(f"{count},{basename}.tag,,{os.path.getsize(xml_file)}\n".encode('ascii'))
            xml_content = read_file(xml_file)
            output.write(xml_content)
            output.write(b"\n")  # Ensure newline after XML content
            count += 1
        else:
            print(f"Warning: {xml_file} not found.")

        if os.path.exists(xml_pcv_file):
            xml_pcv_content = read_file(xml_pcv_file)
            write_entry(output, count, xml_pcv_file, xml_pcv_content)
            count += 1
        else:
            print(f"Warning: {xml_pcv_file} not found.")

    print(f"Output written to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mkpjw.py <project_name> [-p]")
        sys.exit(1)

    basename = sys.argv[1]
    compress = "-p" in sys.argv
    main(basename, compress)
