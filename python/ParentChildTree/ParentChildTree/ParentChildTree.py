from ctypes import *
import subprocess
import sys

#def LaunchProcess(processPath, processType):
#    print ('1st param '+processPath)
#    print ('2st param '+processType)
    
#    command = [processPath]
#    if(processType == 'p'):
#        #launch child
#        arguments = ["c"]
#        command.extend(arguments)
#        subprocess.Popen(command)
#    else:
#        #launch parent
#        arguments = ["p"]
#        command.extend(arguments)
#        subprocess.Popen(command)

##Get the command line parameters
#inputProcessPath = sys.argv[1]
##print ('1st param '+inputProcessPath)

##launch the process in loop
#LaunchProcess(inputProcessPath,inputParameter)

inputProcessPath = sys.argv[0]
print(inputProcessPath)
subprocess.call(inputProcessPath)
windll.kernel32.TerminateProcess(windll.kernel32.GetCurrentProcess(),0);
