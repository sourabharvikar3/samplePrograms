import subprocess
import csv
import sys
import os
import json
import pefile
from datetime import datetime


######### GLOBALS #########
File_Scanned = 0
PE_File_Scanned = 0
Non_PE_File_Scanned = 0
Signed_File_Scanned = 0
UnSigned_File_Scanned = 0

######### CLASS #########
class DigitalSignatureCheck:

    #Commandline input
    _SIGCHECK_EXE = '.\sigcheck64.exe'
    _SIGCHECK_ARGS = ' -i -h'

    #output files
    _OUTPUTFILENAME = ".\\DigiSigLogData.csv.txt"
    _DigiSigLOG = ".\\DigiSigExecLog.txt"

    #extract record information
    _DIGISIG_KEY_LIST = ["Verified","Link date","Signing date","Catalog","Signers","Cert Status","Valid Usage",
                         "Cert Issuer","Serial Number","Thumbprint","Algorithm","Valid from","Valid to","Company",
                         "Description","Product","Prod version","File version","MachineType","MD5","SHA1","SHA256","IMP",]
    _DIGISIG_DATA_RECORD = {
        "Verified": "n/a", "Link date": "n/a", "Signing date": "n/a", "Catalog": "n/a", "Signers": "n/a", "Cert Status": "n/a",
        "Valid Usage": "n/a", "Cert Issuer": "n/a", "Serial Number": "n/a", "Thumbprint": "n/a", "Algorithm": "n/a", "Valid from": "n/a",
        "Valid to": "n/a", "Company": "n/a", "Description": "n/a", "Product": "n/a", "Prod version": "n/a", "File version": "n/a",
        "MachineType": "n/a", "MD5": "n/a", "SHA1": "n/a", "SHA256": "n/a", "IMP": "n/a"
                    }
    _DIGISIG_DATA = {}

    Delimiter = "|"
    IsHeaderPresent = False

    #Catalog file path
    CatRootFolderWin32 = "C:\WINDOWS\system32\CatRoot"
    CatRoot2FolderWin32 = "C:\WINDOWS\system32\catroot2"
    CatRootFolderSysWow64 = "C:\WINDOWS\SysWOW64\catroot"
    CatRoot2FolderSysWow64 = "C:\WINDOWS\SysWOW64\catroot2"

    def check_pe(self, filepath):

        #Check if file is PE file
        #Check if security directory exists

        try:
            VirtualAddress = 0
            Size = 0
            pefile_handle = pefile.PE(name=filepath, fast_load=True)
            pefile_handle.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_SECURITY']])
            for s in pefile_handle.__structures__:
                if s.name == 'IMAGE_DIRECTORY_ENTRY_SECURITY':
                    # set the offset to the signature table
                    VirtualAddress = s.VirtualAddress
                    # set the length of the table
                    Size = s.Size
                    break

            pefile_handle.close()

            if Size != 0:
                #PE, Signed
                return  (True, True)
            else:
                #PE, Unsigned
                return (True, False)
        except:
            # NonPE, Unsigned
            return (False, False)


    def log(self, msg):
        print (msg)
        with open(self._DigiSigLOG, "a")as logfile:
            logfile.write(msg + "\n")

    def WriteToOutput(self, header_flag):

        #Write content to Output file using delimiter
        delimiter = self.Delimiter
        Output_list = []
        if header_flag == True:
            with open(self._OUTPUTFILENAME, "a") as outfile:
                outfile.write(delimiter.join(sorted(self._DIGISIG_DATA.keys())) + "\n")

        for key in sorted(self._DIGISIG_DATA.keys()):
            value = ("\"%s\"")%(self._DIGISIG_DATA[key])
            Output_list.append(value)
        with open(self._OUTPUTFILENAME,"a") as outfile:
            outfile.write(delimiter.join(Output_list)+"\n")

    def parse_sigcheck_output(self, filetoscan, output):

        global File_Scanned
        global PE_File_Scanned
        global Non_PE_File_Scanned
        global Signed_File_Scanned
        global UnSigned_File_Scanned

        self._DIGISIG_DATA = dict(self._DIGISIG_DATA_RECORD)
        result = output.split("\r\n")
        #result = output
        signers_sig_flag = 0

        for line in result:
            msg = self._DIGISIG_DATA["Verified"] + " " + line
            #self.log(msg)
            if len(line.split(":")) == 2:
                #Key valur pair is present
                key = line.split(":")[0].strip("\t")
                value = line.split(":")[1].strip("\t")
                #print key , value
                if key in self._DIGISIG_KEY_LIST:
                    if self._DIGISIG_DATA[key] == "n/a":
                        if key == "Signers":
                            signers_sig_flag = signers_sig_flag + 1
                        else:
                            self._DIGISIG_DATA[key] = value
            elif (line.strip(" ") != "") and len(line.split(":")) == 1 and signers_sig_flag == 1:

                #Get Signers information
                publisher_value = line.strip("\t").strip(" ")
                self._DIGISIG_DATA[key] = publisher_value

                signers_sig_flag = signers_sig_flag + 1
            elif len(line.split(":")) > 2:
                other_fields = ["Catalog","Valid from","Valid to", "Link date", "Signing date"]

                key = line.split(":")[0].strip("\t")
                #print line.split(":")[1:]
                if key in other_fields:
                    value = ":".join(line.split(":")[1:]).strip("\t")
                    #print value
                    self._DIGISIG_DATA[key] = value

        self._DIGISIG_DATA["Filepath"] = filetoscan

        (IsPEfile, IsPESigned) = self.check_pe(filetoscan)
        self._DIGISIG_DATA["IsPEfile"] = IsPEfile
        self._DIGISIG_DATA["IsPESignedfile"] = IsPESigned
        if IsPEfile:
            PE_File_Scanned = PE_File_Scanned + 1
        else:
            Non_PE_File_Scanned = Non_PE_File_Scanned + 1

        if self._DIGISIG_DATA["Verified"] == "Signed":
            Signed_File_Scanned = Signed_File_Scanned + 1

            if self._DIGISIG_DATA["Filepath"].lower() == self._DIGISIG_DATA["Catalog"].lower():
                self._DIGISIG_DATA["HasCatalog"] = False
            else:
                self._DIGISIG_DATA["HasCatalog"] = True

            if (self.CatRootFolderWin32.lower() in self._DIGISIG_DATA["Catalog"].lower()) or\
                    (self.CatRoot2FolderWin32.lower() in self._DIGISIG_DATA["Catalog"].lower()) or\
                    (self.CatRootFolderSysWow64.lower() in self._DIGISIG_DATA["Catalog"].lower()) or\
                    (self.CatRoot2FolderSysWow64.lower() in self._DIGISIG_DATA["Catalog"].lower()):
                self._DIGISIG_DATA["CatRootInPath"] = True
            else:
                self._DIGISIG_DATA["CatRootInPath"] = False
        else:
            UnSigned_File_Scanned = UnSigned_File_Scanned + 1
            self._DIGISIG_DATA["HasCatalog"] = "n/a"
            self._DIGISIG_DATA["CatRootInPath"] = "n/a"

        #self.log(str(self._DIGISIG_DATA))
        if os.path.exists(self._OUTPUTFILENAME):
            self.WriteToOutput(False)
        else:
            self.WriteToOutput(True)
            #print line.strip("\t")

    def run(self, filetoscan):

        signature_cnt = 4
        global File_Scanned
        ExceptionOccured = False
        cmd = ("%s %s \"%s\"") % (self._SIGCHECK_EXE, self._SIGCHECK_ARGS, filetoscan)

        self.log('\nRunning command: %s' % cmd)

        try:
            result = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as e:
            #self.log(str(e))
            if e.returncode < 0:
                self.log(str(e))
                ExceptionOccured = True
            else:
                result = e.output
                #print result

        if not ExceptionOccured:
            try:
                File_Scanned = File_Scanned + 1
                str1 = str(result)
                signature_cnt = str1.count("Signers:")
                #self.parse_sigcheck_output(filetoscan, str1)
                #self.log("Scan Completed...")
            except Exception as e:
                self.log(str(e))

        result = ""
        self._DIGISIG_DATA = {}
        return signature_cnt
