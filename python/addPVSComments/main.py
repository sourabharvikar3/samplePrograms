import os

comment1_to_add = "// This is a personal academic project. Dear PVS-Studio, please check it.\n"
comment2_to_add = "// PVS-Studio Static Code Analyzer for C, C++, C#, and Java: https://pvs-studio.com\n"

target_path = r"E:\repo\qagent\yara\Source\Agent\IOC"

def prepend_multiple_lines(file_name, list_of_lines):
    # define name of temporary dummy file
    dummy_file = file_name + '.bak'
    # open given original file in read mode and dummy file in write mode
    with open(file_name, 'r') as read_obj, open(dummy_file, 'w') as write_obj:
        # Iterate over the given list of strings and write them to dummy file as lines
        for line in list_of_lines:
            write_obj.write(line + '\n')
        # Read lines from original file one by one and append them to the dummy file
        for line in read_obj:
            write_obj.write(line)
    # remove original file
    os.remove(file_name)
    # Rename dummy file as the original file
    os.rename(dummy_file, file_name)

def ImplementPVsComments(dir):
    list_of_lines = [comment1_to_add,comment2_to_add]
    try:
        for file in os.listdir(dir):
            curr_file_path = dir + "\\" + file
            if os.path.isdir(curr_file_path):
                ImplementPVsComments(curr_file_path)
            else:
                if file.endswith(".cpp"):
                    prepend_multiple_lines(curr_file_path, list_of_lines)
    except:
        return

def main():
    ImplementPVsComments(target_path)

if __name__ == "__main__":
    main()
