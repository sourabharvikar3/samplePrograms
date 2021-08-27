import os
import subprocess, sys

target_path = r"C:\Users\sarvikar\Documents\fileSet\script"

def RunScript(script_file):
    p = subprocess.Popen("cmd.exe Unblock-File " + script_file)
    p = subprocess.Popen("powershell.exe -ExecutionPolicy UnRestricted " + script_file, stdout=sys.stdout)
    p.communicate()

def EnumAndExecutePS():
    try:
        for file_name in os.listdir(target_path):
            current_file_path = target_path + "\\" + file_name
            if os.path.isfile(current_file_path) and file_name.endswith(".ps1"):
                RunScript(current_file_path)
    except Exception as e:
        print(str(e))

def main():
    while(1):
        EnumAndExecutePS()

if __name__ == "__main__":
    main()