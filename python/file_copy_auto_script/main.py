
import os
import win32api
from shutil import copyfile
from genericpath import exists

target_dir = r"c:\testfiles"

def CopyFile(src_file,file_name):
    dest_file = target_dir + "\\" + file_name
    if not os.path.exists(dest_file):
        copyfile(src_file, dest_file)

def StartTestingLoop(source_dir):
    try:
        while 1:
            #clean target dir
            for x in os.listdir(target_dir):
                file_path = target_dir + "\\" + x
                os.remove(file_path)

            #start copy operations
            for x in os.listdir(source_dir):
                file_path = source_dir + "\\" + x
                CopyFile(file_path, x)
    except:
        return

def main():
    source_dir = r"Z:\FileSet1"
    StartTestingLoop(source_dir)

if __name__ == "__main__":
    main()