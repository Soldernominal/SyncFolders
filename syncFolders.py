''' One way periodically performed sync of two folders
    Record creation/copying/removal of file to: cmd(output), log file
    Input: folder paths(master and copy), sync interval, log file path
    Output: Info about file creation/copying/removal

   Notes: master can't be compared to slave folder, only to the prev iteration of itself: else master changes in regard to slave
'''
import os
import time
import shutil

def check_folderpath(folderpath):
    if not os.path.isdir(masterfolder_path):
        raise Exception("Invalid folder path")
    pass

def makefolder_ifnone(folderpath):
    if not os.path.exists(folderpath):
        os.mkdir(folderpath) 
    pass

def check_files(folderpath):
    global oldmasterfiles
    folderfiles = os.listdir(folderpath)
    if len(folderfiles)!=len(oldmasterfiles):
        for file in folderfiles:
            shutil.move(folderpath + file, slavefolder_path + file)
    oldmasterfiles = folderfiles

# synchronises slave with master by copying the files from master folder
def sync(masterfolder_path, slavefolder_path):
    masterfiles = os.listdir(masterfolder_path)
    slavefiles = os.listdir(slavefolder_path)
    for file in slavefiles:
        try:
            shutil.rmtree(os.path.join(slavefolder_path, file))
        except OSError:
            os.remove(os.path.join(slavefolder_path, file))
    for file in masterfiles:
        try:
            shutil.copyfile(os.path.join(masterfolder_path, file), os.path.join(slavefolder_path, file))
        except:
            shutil.copytree(os.path.join(masterfolder_path, file), os.path.join(slavefolder_path, file))	# for folders, as they are restricted for copyfile

# write changes into log.txt
def editloginfo(newinfo):
    global logfile_path
    newinfo+= "\n"
    with open(logfile_path, "a") as log:
        log.write(newinfo)

# when the file is deleted/created, record into log.txt/cmd prompt
def record(masterfolder_path):
    global old_masterfiles
    masterfiles = os.listdir(masterfolder_path)
    timenow = time.strftime("%H:%M", time.localtime())
    for filename in masterfiles:	# check file creation
        if filename not in old_masterfiles:
            newinfo = timenow + " - " + filename + " Was CREATED"
            print(newinfo)
            editloginfo(newinfo)
    for filename in old_masterfiles:	# check file deletion
        if filename not in masterfiles:
            newinfo = timenow + " - " + filename + " Was DELETED"
            print(newinfo)
            editloginfo(newinfo)
    newinfo = timenow + " - " + "All Files Copied Successfully"
    print(newinfo)
    editloginfo(newinfo)

# input and init parameters
masterfolder_path = input("Please, input path of the master folder: ")
slavefolder_path = input("Please, input path of the folder to be synchronized: ")
sync_interval = float(input("Please, input the time delay of sync(in seconds): "))
logfile_path = input("Please, input the path of your log file (path+log.txt): ")

# create paths if dont exist
makefolder_ifnone(masterfolder_path)
makefolder_ifnone(slavefolder_path)
if not os.path.exists(logfile_path):
    open(logfile_path, "a") 

# check validity of folder paths
check_folderpath(masterfolder_path)
check_folderpath(slavefolder_path)
check_folderpath(logfile_path)

# in case we write in the log same file, this will distinguish new part by a date
datenow = time.strftime("%Y-%m-%d", time.localtime())
with open(logfile_path, "a") as log:
    log.write("-"*14 + datenow + "-"*14 + "\n")

# main loop
while 1:
    old_masterfiles = os.listdir(masterfolder_path)	# Check current iteration of files in master folder, record and then wait for changes(hence timer below this)
    time.sleep(sync_interval)
    makefolder_ifnone(masterfolder_path)
    makefolder_ifnone(slavefolder_path)
    if not os.path.exists(logfile_path):
        open(logfile_path, "a") 
    sync(masterfolder_path, slavefolder_path)
    record(masterfolder_path)
