import os 
from win32api import GetFileVersionInfo, LOWORD, HIWORD

class RuleInfo:
    file = ''
    name = ''
    description = ''
    strings = []
    #conditions = [] 

g_name_cnt = 1
g_name = "RuleName_"

g_description_cnt = 1
g_description = "RuleDescription_"

g_string_len = 4
g_string_len_max = 8
g_string_len_min = 4

g_string_cnt_min = 3
g_string_cnt_max = 6
g_string_cnt = 3

g_condition_or = 0 

def litering_by_two(a):
    return ' '.join([a[i:i + 2] for i in range(0, len(a), 2)])

def get_version_number(filename):
    try:
        info = GetFileVersionInfo (filename, "\\")
        ms = info['FileVersionMS']
        ls = info['FileVersionLS']
        return "\"" + str(HIWORD (ms)) + "." + str(LOWORD (ms)) + "." + str(HIWORD (ls)) + "." + str(LOWORD (ls)) + "\" wide ascii"
    except:
        return "\"" + "0.0.0.0" + "\" wide ascii"

def CreateYaraRule(file_path, file_name):
    global g_name
    global g_name_cnt
    global g_description
    global g_description_cnt
    global g_string_cnt
    global g_string_len
    global g_string_len_min
    global g_string_len_max

    rule = RuleInfo()
    local_string_cnt = 0

    rule.file = file_name
    rule.name = g_name + str(g_name_cnt) #+ "__" + file_name
    rule.description = g_description + str(g_description_cnt)

    g_name_cnt = g_name_cnt + 1
    g_description_cnt = g_description_cnt + 1 

    result = ""
    f = open(file_path, "rb")
    try:
        rule.strings.clear()
        for x in range(g_string_cnt):
            f.seek(x + 258 + g_string_len)
            read_str = f.read(g_string_len)
            result1 = litering_by_two(read_str.hex())
            
            if len(result1) == 0:
                return None

            result_str = "{ " + result1 + " }"
            rule.strings.append(result_str)
        rule.strings.append(get_version_number(file_path))
        rule.strings.append("\"" + file_name + "\" wide ascii")
    except:
        print("Exception")

    f.close()

    g_string_cnt = g_string_cnt + 1
    g_string_len = g_string_len + 1

    if g_string_cnt > g_string_cnt_max:
        g_string_cnt = g_string_cnt_min

    if g_string_len > g_string_len_max:
        g_string_len = g_string_len_min

    return rule

def DumpRuleInFile(rule):
    yara_rule_file = r".\rule.yar"
    rule_file = open(yara_rule_file,"a")

    rule_file.write("rule " + rule.name + " {\n")
    
    rule_file.write("\tmeta:\n")
    rule_file.write("\t\tdescription = \"" + rule.file + "\"\n")
    
    rule_file.write("\tstrings:\n")
    i = 0
    for string in rule.strings:
        content = "\t\t$string_" + str(i) + " = " + str(string) + "\n"
        rule_file.write(content)
        i = i + 1

    rule_file.write("\tcondition:\n")
    i = 0
    rule_file.write("\t\t")
    for string in rule.strings:
        if i != 0:
            rule_file.write(" and ")    
        rule_file.write("$string_" + str(i))
        i = i + 1

    rule_file.write("\n}\n")
    rule_file.close()

def CreateYarFile(sample_file_dir):
    try:
        for x in os.listdir(sample_file_dir):
            file_path = sample_file_dir + "\\" + x
            rule = CreateYaraRule(file_path, x)
            if rule is not None:
                DumpRuleInFile(rule)
            del rule
    except:
        return

def main():
    sample_file_dir = r"C:\Users\sarvikar\Desktop\temp\Yara\FileSet\DetectlableFiles"
    CreateYarFile(sample_file_dir)

if __name__ == "__main__":
    main()