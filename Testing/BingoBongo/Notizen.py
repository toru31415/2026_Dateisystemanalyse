# region Funktion mit shutil  UPDATE 10.02.2026
# https://docs.python.org/3/library/shutil.html

# Warning Even the higher-level file copying functions (shutil.copy(), shutil.copy2()) cannot copy all file metadata.
# On POSIX platforms, this means that file owner and group are lost as well as ACLs. On Mac OS, the resource fork and other metadata are not used.
# This means that resources will be lost and file type and creator codes will not be correct. On Windows, file owners, ACLs and alternate data streams are not copied.

import shutil
TestPath = "/home/fon/Documents/"
print(shutil.disk_usage(TestPath))

# endregion Funktion mit shutil  END UPDATE 10.02.2026  

# region Variante mit os modul UPDATE 10.02.2026 
# Source - https://stackoverflow.com/a/1392549
# Posted by monkut, modified by community. See post 'Timeline' for change history
# Retrieved 2026-02-10, License - CC BY-SA 4.0

# import os

# def get_size(start_path = '.'):
#     total_size = 0
#     for dirpath, dirnames, filenames in os.walk(start_path):
#         for f in filenames:
#             fp = os.path.join(dirpath, f)
#             # skip if it is symbolic link
#             if not os.path.islink(fp):
#                 total_size += os.path.getsize(fp)

#     return total_size

# print(get_size(), 'bytes')
# endregion Variante mit os modul UPDATE 10.02.2026

# region Variante mit shutil modul UPDATE 10.02.2026 
# Source - https://stackoverflow.com/a/79483151
# Posted by LLefevre
# Retrieved 2026-02-10, License - CC BY-SA 4.0

# import shutil
# stat = shutil.disk_usage(TestPath)
# endregion Variante mit shutil modul UPDATE 10.02.2026

# region Variante mit pathlib und itertools modul UPDATE 10.02.2026 
# Source - https://stackoverflow.com/a/76367875
# Posted by Csaba K.
# Retrieved 2026-02-10, License - CC BY-SA 4.0

# from pathlib import Path
# from itertools import tee


# def scandir(p: Path) -> int:
#   files, dirs = tee(Path(p).iterdir())
#   total = sum(x.stat().st_size for x in files if x.is_file())
#   total += sum(scandir(x) for x in dirs if x.is_dir())
#   return total
  
  
# print(scandir(TestPath))  # path size in bytes
# endregion Variante mit pathlib und itertools modul UPDATE 10.02.2026 