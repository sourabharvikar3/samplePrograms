import os
import re

def GetCodeFileList(input_dir, files):
    dir_files = os.listdir(input_dir)

    full_paths = map(lambda name: os.path.join(input_dir, name), dir_files)

    for file in full_paths:
        if os.path.isfile(file) and (file.endswith('.h') or file.endswith('.c') or file.endswith('.cpp') or file.endswith('.pt') ):
            files.append(file)
        if os.path.isdir(file) and not file.endswith('.vs'):
            files.append(GetCodeFileList(file, files))

    return files

def GetMemTagLines(file, mem_tags):
    file_to_read = open(file, 'r')
    Lines = file_to_read.readlines()

    file_to_read.close()

    for line in Lines:
        if re.search('^#define.*\'....\'$', line):
            mem_tags.append(line)


def GetMemTags(mem_tag_lines, mem_tags):
    for line in mem_tag_lines:
        sub_Str = re.search('\'....\'', line)
        if sub_Str:
            mem_tags.append((line[sub_Str.start()+1:sub_Str.end()-1])[::-1])

dir_to_scan = 'C:\\repo\\qagentdvr\\Source'
files = []
mem_tag_lines = []
mem_tags = []

GetCodeFileList(dir_to_scan, files)

for file in files:
    if not isinstance(file, list):
        GetMemTagLines(file, mem_tag_lines)

GetMemTags(mem_tag_lines, mem_tags)

#print(*mem_tags, sep =  "\n")

mem_tags_no_dup = []
for i in mem_tags:
    if i not in mem_tags_no_dup:
        mem_tags_no_dup.append(i)

file_write = open(r"C:\\Users\\sarvikar\\Desktop\\temp\\memtag.txt",'w')
for tag in mem_tags_no_dup:
    file_write.write(tag + "\n")
file_write.close()

#open pool files
pool_files = []
GetCodeFileList("C:\\Users\\sarvikar\\Desktop\\temp\\CRM\\CRM-80380\\poolmoon", pool_files)

tag_from_pool = []
for pool_file in pool_files:
    f_read = open(pool_file,'r')
    lines = f_read.readlines()

    for line in lines:
        for tag in mem_tags_no_dup:
            fnd = re.search(tag,line)
            if fnd:
                tag_from_pool.append(line)

#print(*tag_from_pool, sep =  "\n")

file_write = open(r"C:\\Users\\sarvikar\\Desktop\\temp\\Qmemtag.txt",'w')
for tag in tag_from_pool:
    file_write.write(tag + "\n")
file_write.close()