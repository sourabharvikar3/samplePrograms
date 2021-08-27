from genericpath import isfile
import os
import pefile
import win32com.client
from digisign import DigitalSignatureCheck
from shutil import copyfile

src_path = r"C:\Users\sarvikar\Documents\fileSet\lessSign1"
destination_path = r"C:\Users\sarvikar\Documents\fileSet\zeroSign"
DigiSig = DigitalSignatureCheck()


def CopyFile(src_file,file_name):
    dest_file = destination_path + "\\" + file_name
    if not os.path.exists(dest_file):
        copyfile(src_file, dest_file)

def IsMultiSign(file_path):
    DigiSig.check_pe(file_path)
    sign_cnt = DigiSig.run(file_path)
    if(sign_cnt>0):
        return True
    return False
    
def start():
    file_cnt = 0
    for file in os.listdir(src_path):
        complete_file = src_path + "\\" + file
        if (os.path.isfile(complete_file)):
            if not IsMultiSign(complete_file):
                file_cnt += 1
                CopyFile(complete_file, file)
    print("File copied " + str(file_cnt))

def main():
    #IsMultiSign(r"C:\Users\sarvikar\Documents\fileSet\CleanFiles1\FileCoAuthLib64.dll")
    start()

if __name__ == "__main__":
    main()