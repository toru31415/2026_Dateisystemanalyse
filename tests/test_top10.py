# aktuellen Ordner erkennen und ausgeben
import os
CurrentWorkingDirectory = os.getcwd() 
print("Current Working Directory:", CurrentWorkingDirectory)

# region import for function to work UPDATE 17.02.2026 
# # function -> create_testfile
# import os
# # function -> et_size
# from pathlib import Path
# # function -> get_file_sha256
# from sys import argv
# from hashlib import sha256
# endregion import for function to work UPDATE 17.02.2026 

# region import custom modules UPDATE 17.02.2026 
import sys
sys.path.insert(1, '/home/fon/Documents/GitHub/2026_Dateisystemanalyse')
from utils import *
# endregion import custom modules UPDATE 17.02.2026 


create_testfile("test2", 1073741824)
get_file_sha256(CurrentWorkingDirectory+"/test2")

