from genericpath import exists
import os
import win32api
from shutil import copyfile

extension = '.dll'
destination = r'C:/Users/sarvikar/Desktop/temp/Yara/FileSet/DLL/'

def CopyFile(src_file,file_name):
    dest_file = destination + file_name
    if not os.path.exists(dest_file):
        copyfile(src_file, dest_file)

def EnumDirAndSave(dir):
    try:
        for x in os.listdir(dir):
            file_path = dir + "\\" + x
            if file_path.endswith(extension):
                CopyFile(file_path, x)
            else:
                if(os.path.isdir(file_path)):
                    EnumDirAndSave(file_path)
    except:
        return

#start the main here
## Enum volumes
drives = win32api.GetLogicalDriveStrings()
drives = drives.split('\000')[:-1]

#EnumDirAndSave("c:\Documents and Settings")

for x in drives:
    EnumDirAndSave(x)