# FolderSuperviser
A python script that oversees a folder. It logs into a specified file all operations (creation, edition, deletion) of files and folders within a specified directories. One can specify the time between two checks, or a maximum level for recursivity (meaning, how deep the superviser will go in the folder's tree).

# Usage
FolderSuperviser [-h] [-d DIRECTORY] [-l LOG] [-t TIME] [-r RECURSIVE]

Arguments:
    
    -h, --help                           Shows this help message and exit
    -d DIRECTORY, --directory DIRECTORY  The directory you want to supervise
    -l LOG, --log LOG                    The log file.
    -t TIME, --time TIME                 Frequency of folder check (in seconds).
    -r RECURSIVE, --recursive RECURSIVE  Depth of recursive folder check. 0 = unlimited.


# Example
One wants to run the program on a folder called "folder", loggings logs in /var/log/superviser/log.txt, with a maximum recursivity of 3 levels, and one check every two seconds. The targetted folder is empty.

    sudo python superviser.py -d folder/ -l /var/log/superviser/log.txt -r 3 -t 2 &

One takes the following actions within folder :

    touch folder/file.txt
    echo "Hello world !" > folder/file.txt 
    mkdir folder/sub1 folder/sub2 folder/sub1/sub11 folder/sub1/sub12
    mv folder/sub1/sub12 folder/sub3
    mv folder/file.txt folder/sub3/file.txt
    mv folder/sub3 folder/sub1/sub12
    rm -rf folder/sub1/sub12


The log files now contains the following logs :

    29/09/2016-15:36:49 INFO Folder superviser started
    29/09/2016-15:36:59 INFO The  file  folder/file.txt has been added
    29/09/2016-15:37:04 INFO The  file  folder/file.txt has been modified.
    29/09/2016-15:37:09 INFO The folder folder/sub1/sub12 has been added.
    29/09/2016-15:37:09 INFO The folder folder/sub1 has been added.
    29/09/2016-15:37:09 INFO The folder folder/sub2 has been added.
    29/09/2016-15:37:09 INFO The folder folder/sub1/sub11 has been added.
    29/09/2016-15:37:19 INFO The folder folder/sub1/sub12 has been moved to folder/sub3.
    29/09/2016-15:37:29 INFO The  file  folder/file.txt has been moved to folder/sub3/file.txt.
    29/09/2016-15:37:39 INFO The folder folder/sub3 has been moved to folder/sub1/sub12.
    29/09/2016-15:37:39 INFO The  file  folder/sub3/file.txt has been moved to folder/sub1/sub12/file.txt.
    29/09/2016-15:37:44 INFO The folder folder/sub1/sub12 has been deleted.
    29/09/2016-15:37:44 INFO The  file  folder/sub1/sub12/file.txt has been deleted.
