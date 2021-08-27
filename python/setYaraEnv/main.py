import sqlite3
from sqlite3.dbapi2 import Cursor, connect
import win32serviceutil
import time
from shutil import copyfile

service_name = "qualysagent"
db_file = r"c:\programdata\qualys\qualysagent\config.db"
sec_to_wait = 5

def StartStopSerice(flag):
    service_state = win32serviceutil.QueryServiceStatus(service_name)

    if(flag):
        if(service_state[1] != 4):
            win32serviceutil.StartService(service_name)
            time.sleep(sec_to_wait)
    else:
        if(service_state[1] == 4):
            win32serviceutil.StopService(service_name)
            time.sleep(sec_to_wait)

    return 1

def ModifyConfigCapiInterval(group, item, value):
    
    sql = '''Update Settings SET Value = ? WHERE [Group] = ? AND [Item] = ?'''
    conn = None
    try:
        conn = sqlite3.connect(db_file)

        cur = conn.cursor()
        cur.execute(sql,(value, group, item))

        conn.commit()
        conn.close()
    except:
        print("exception while openging db file")
        return 0

    return 1

def ModifyManifestTable():
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        sql = '''Insert INTO Manifests (ManifestId,CurrentState,ScanIntervalSeconds,LastEventScan,DeltaId,LastEventDeltaUpload,ManifestType,UploadStartFragment,SnapshotHash,Flags,FilePath,SchemaVersion) 
            values (?,?,?,?,?,?,?,?,?,?,?,?)'''

        cur = conn.cursor()
        cur.execute(sql,("{509150AA-90D9-45A9-AA10-5464DB8331B6}","1","60","2021-07-19 11:47:22.886","{00000000-0000-0000-0000-000000000000}","2021-07-19 05:43:08.465","EDR_YARA",0,0,2,"C:\ProgramData\Qualys\QualysAgent\Manifests\{509150AA-90D9-45A9-AA10-5464DB8331B6}.db","3"))

        conn.commit()
        conn.close()
    except:
        print("exception while openging db file")
        return 0

    return 1
   

def PlaceYaraManifest():
    copyfile(".\{509150AA-90D9-45A9-AA10-5464DB8331B6}.db", 
    r"C:\ProgramData\Qualys\QualysAgent\Manifests\{509150AA-90D9-45A9-AA10-5464DB8331B6}.db")

    return 1

def main():
    # Stop the service
    result = StartStopSerice(0)
    if(result != 1): return 0

    #Add new manifest in table
    result = ModifyManifestTable()
    if(result != 1): return 0

    #Place manifest in the required directory
    result = PlaceYaraManifest()
    if(result != 1): return 0

    # modify config capi interval
    result = ModifyConfigCapiInterval("CAPI","INTERVAL",7200)
    if(result != 1): return 0

    # start the service now
    result = StartStopSerice(1)
    if(result != 1): return 0

    print("Required changes are done, Note this changes will be valid for 2 hours only")

if __name__ == "__main__":
    main()