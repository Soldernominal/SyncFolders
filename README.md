# SyncFolders
A python code that synchronizes two repositories.
A one way, master to replica folder synchronization with a time delay, with all file deletion/creation/copy to be recorded in the .txt file (with some name of choice) and in the cmd prompt.

The code uses 3 libraries in total: os, time and shutil. The program copies all files after a time delay set by the user, and replaces all existing replica folder files with copies.
A special error is raised if the path doesn't exist. I decided to only show changes to the master folder, as the replica will synchronize with it eventually anyway.
If changes to the replica folder are also desired, I can add them. I did not know if I should override the existing log.txt content, but ultimately decided to keep the existing records, as they may be important.
Hence, the app separates each new session in the log.txt with a date. 
