# Enthält wiederverwendbare Funktionen.

# region function -> create_testfile UPDATE 17.02.2026 
from os import os
def create_testfile(name, size): # Source - https://stackoverflow.com/a/8816144
    file = open(name, "wb")
    file.seek(size-1)
    file.write(b"\0")
    file.close()
    print(os.stat(name).st_size)
# endregion function -> create_testfile UPDATE 17.02.2026 

# region function -> et_size UPDATE 17.02.2026 
from pathlib import Path
def get_size(folder: str) -> int:
    return sum(p.stat().st_size for p in Path(folder).rglob('*'))
# endregion function -> et_size UPDATE 17.02.2026 

# region function -> get_file_sha256 UPDATE 17.02.2026 
from sys import argv
from hashlib import sha256
def get_file_sha256(file):
    # Construct an sha256 algorith
    h256 = sha256()

    # Get the name of the file we want to hash
    fname = file

    # Read the contents of the file into the hash algorithm
    h256.update(open(fname,'rb').read())

    # Print the digest/hash of the file's contents
    print (h256.hexdigest())
# endregion function -> get_file_sha256 UPDATE 17.02.2026 