#!/usr/bin/env python3
import os
import gzip
"""
The purpose of this program is to systematicly search for PLC 
element patterns. the search range is limited, for now (16). 
of course there are many features to add.
in an original decompressed source file, 
We are searching for the know entity, E903 normaly open contactor.
( I know it is there, because I put it there )

Having real source files would be handy. 
Test files are designed around doing frequency analysis right now, 
and are not practical programs.

then generating an output file with the name of the change,  
and recompressing it, and changing the name to WindLDR pjw 

of course, I dont know what all the symbols are, this script is 
to help systematicly identify possible symbol occurances. 
The output of which may generate errors, or invalid entries, 
I dont know what it will do yet, which is sort of the point. 
"""
def replace_pattern_in_binary(input_file_path, pattern, replacements):
    with open(input_file_path, 'rb') as f:
        binary_data = f.read()

    base_name, ext = os.path.splitext(input_file_path)

    for replacement in replacements:
        new_data = binary_data.replace(pattern, replacement)
        output_file_path = f"{replacement.hex()}{ext}"

        # Write the modified data to a temporary file
        with open(output_file_path, 'wb') as out_f:
            out_f.write(new_data)

        # Compress the output file using gzip
        compressed_output_path = output_file_path + '.gz'
        with open(output_file_path, 'rb') as f_in, gzip.open(compressed_output_path, 'wb') as f_out:
            f_out.writelines(f_in)

        # Rename the compressed file to have a .pjw extension
        final_output_path = f"{replacement.hex()}.pjw"
        os.rename(compressed_output_path, final_output_path)

        # Remove the temporary uncompressed file
        os.remove(output_file_path)

        print(f"Created {final_output_path}")

# Define the input file and the pattern to replace
input_file_path = 'c'
pattern = bytes.fromhex('E903')

# Generate replacements E003 to EF03
replacements = [bytes([0xE0 + i, 0x03]) for i in range(16)]

replace_pattern_in_binary(input_file_path, pattern, replacements)

