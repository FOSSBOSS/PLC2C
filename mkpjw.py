#!/usr/bin/env python3
import os
import sys
import gzip
"""
Usage:
mkpjw.py project_name
or
mkpjw  project_name -p

Produce a pjw file using file constituents, as available.
the only one required is a *.ldr, which is the actual 
program file section. Everything else is config.

It works**, but there is some nuances.

Ill extend it when I figure out what Im doing with individual sections
deconstruction, and reconstructions.
"""
def read_file(file_path):
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'rb') as f:
        return f.read()

def write_entry(output, count, file_name, content):
    if content is not None:
        output.write(f"{count},{file_name},,{len(content)}\n".encode('ascii'))
        output.write(content)

def main(basename, compress=False):
    files_to_process = [
        "CommentDownloadSettings.ini",
        f"{basename}.bmk",
        f"{basename}.cmt",
        f"{basename}.cod",
        f"{basename}.ldr",
        f"{basename}.oub",
        f"{basename}.tag",  #fix this
        f"{basename}.xml"
    ]

    count = 0
    output_file = f"{basename}.pjw" if compress else f"{basename}"

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

            if file_name.endswith(".bmk"):
                output.write(b"\x00\x00")  # Write 2 NULL bytes after .bmk file

            count += 1

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py <project_name> [-p]")
        sys.exit(1)

    basename = sys.argv[1]
    compress = "-p" in sys.argv
    main(basename, compress)
