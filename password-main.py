## Imports and Global Variables 
import sys ## Allows sys file manipulation
import argparse ## Allows additional python arguments
from pathlib import Path ## Allows additional pathing support
import lzma ## Allows for extra compression handling
import shutil ## Allows for moving files

## py7zr lives in this project's own venv (lib/<ver>/site-packages), not installed system-wide.
## If the current interpreter can't find it, point sys.path at the local copy first.
try:
    import py7zr ## Allows 7zip access
except ImportError:
    _venv_root = Path(__file__).resolve().parent
    for _lib in sorted((_venv_root / "lib").glob("python*")):
        _site_packages = _lib / "site-packages"
        if (_site_packages / "py7zr").is_dir():
            sys.path.insert(0, str(_site_packages))
            break
    import py7zr ## Allows 7zip access

## Global Variables and Lists
successes = []
failures = []

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

    for count, pw in enumerate(read_passwords(sys.argv[1]), start=1): ## Begin loop, do not end until finished with list.
        try:
            with py7zr.SevenZipFile('lockedzip.7z', 'r', password=pw) as testzip: ## Recursively test for success/failed attempts
                bad_file = testzip.testzip() ## Failed ZIPS form damaged archives will end up here.
            if bad_file is None:  ## If no errors, print a success and append to index.
                print(f"SUCCESS: {pw}")
                successes.append(pw)
            else:
                print(f"{pw} failed (bad file: {bad_file})") ## Catalogue and append unsuccessful attempt.
                failures.append(pw)
        except Exception as e:
            print(f"{pw} failed ({type(e).__name__}) --INCORRECT_PASSWORD--")
            failures.append(pw)

## Extract upon successful entry added to index. New directory is made, and all results including the success and pass log go here.
if successes:
    real_pw = successes[0]
    with py7zr.SevenZipFile('lockedzip.7z', 'r', password=real_pw) as z:
        z.extract('Results')

## Print total success/failure count.
print(f"\n{len(successes)} succeeded, {len(failures)} failed") 

## Record to results.txt in results directory
try:
    with open("results.txt", "w") as f:
        f.write("PASSLOG, Success and Fail Count\n" + "Successful Passwords Here\n" + str(successes) + "\n\n" + "Failed Passwords Here\n" + str(failures))
        shutil.move("./results.txt", "./Results/results.txt")
except FileNotFoundError:
    with open("results.txt", "x") as f:
        f.write("PASSLOG, Success and Fail Count\n" + str(successes) + "\n\n" + str(failures))
        shutil.move("./results.txt", "./Results/results.txt")

## File Description: A recursive script that allows for the use of a dictionary to catalogue failed and successful decompression
## attempts while also providing a successful exctraction of the archive's contents.

## Author: Moxxii Sutton