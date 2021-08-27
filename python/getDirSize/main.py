import os
from os import path

def get_directory_size(directory):
    #Returns the directory size in bytes
    total = 0

    try:
        for entry in os.scandir(directory):
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_directory_size(entry.path)

    except NotADirectoryError:
        return os.path.getsize(directory)

    except PermissionError:
        return 0

    return total


size = get_directory_size("C:\\")
print("size:" , size / (1024 * 1024 * 1024), "GB" )