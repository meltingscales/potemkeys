import os
import argparse
import shutil

parser = argparse.ArgumentParser(description='Remove the EOF character (ASCII 26 or 0x1A) from the end of a file.'
                                             'It will copy it to a file with the "no-trailing-eof" extension.'
                                             'Try using the "test-delete-eof.txt" file.')
parser.add_argument('--file', help='File to remove the trailing EOF from.')

EOF = 26

args = parser.parse_args()

if not args.file:
    raise Exception("No file specified. Use --help.")

if not os.path.exists(args.file):
    raise Exception("File " + args.file + " does not exist.")

output_file = args.file + ".no-trailing-eof"

# delete output file if it exists
if os.path.exists(output_file):
    os.remove(output_file)
    print("Deleting " + output_file + " as it exists and we will output to it.")

i = 0
input_file_size_bytes = os.path.getsize(args.file)
print(f"Input file is {input_file_size_bytes} bytes long.")

with open(output_file, 'wb') as of:  # output file.
    with open(args.file, 'rb') as inf:  # input file.
        for inputByte in inf.read():
            print(f"i={i}, byte={(inputByte):4d} aka '{chr(inputByte)}'")

            if (input_file_size_bytes - 1) is i:  # we are at the end
                print("At the end. If the current byte is equal to 26/0x1A, we will NOT write it.")

                if inputByte is EOF:
                    print("The last byte is 26, AKA EOF. Not writing it.")
                else:
                    print(
                        f"The last byte is {(inputByte):4d}, aka '{chr(inputByte)}'. Writing it."
                        f"There is NO trailing EOF in this file.")

                    of.write(chr(inputByte).encode())

            else:  # not at the end. write byte.
                of.write(chr(inputByte).encode())

            i += 1

print("Done. Your file without a trailing EOF can be viewed at " + output_file)
