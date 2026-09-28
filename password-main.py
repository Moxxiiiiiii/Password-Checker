## Imports and Global Variables
import sys ## Allows sys file manipulation
import argparse ## Allows additional python arguments
from pathlib import Path ## Allows additional pathing support
import py7zr ## Allows 7zip access

## Function for recursively reading and yielding passwords
def read_passwords(path):
    """Yield each password from a file, one per line."""
    # errors="ignore" avoids crashes on odd bytes common in large wordlists
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            password = line.rstrip("\r\n")  # Strip newline only, keep spaces
            if password:                    # If true, yields
                yield password

if __name__ == "__main__": # Entry point for password file and body of script
    if len(sys.argv) != 2: # Error for incorrect use of entry
        print(f"Usage: python {sys.argv[0]} <password_file>")
        sys.exit(1)

    try:
        for count, pw in enumerate(read_passwords(sys.argv[1]), start=1):
            print(f"{count}: {pw}")
            with py7zr.SevenZipFile('lockedzip.7z', 'r', password=read_passwords(sys.argv)) as testzip:
                testzip.extract('Results')
    except FileNotFoundError:
        print(f"File not found: {sys.argv[1]}")
        sys.exit(1)
