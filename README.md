# FolderSuperviser
A python script that oversees a folder. It logs into a specified file all operations (creation, edition, deletion) of files and folders within a specified directories. One can specify the time between two checks, or a maximum level for recursivity (meaning, how deep the superviser will go in the folder's tree).

# Usage
FolderSuperviser [-h] [-d DIRECTORY] [-l LOG] [-t TIME] [-r RECURSIVE]

This program will let you know every addition, deletion, and modification within a specified folder.

optional arguments:
  -h, --help
			Show this help message and exit
  -d DIRECTORY, --directory DIRECTORY
                        The directory you want to supervise
  -l LOG, --log LOG
			The log file.
  -t TIME, --time TIME
			Frequency of folder check (in seconds).
  -r RECURSIVE, --recursive RECURSIVE
                        Depth of recursive folder check. 0 = unlimited.


# Example
One wants to run the program on a folder called "folder", loggings logs in /var/log/superviser/log.txt, with a maximum recursivity of 3 levels, and one check every two seconds. The targetted folder is empty.

sudo python superviser.py -d folder/ -l /var/log/superviser/log.txt -r 3 -t 2 &


One takes the following actions within folder :
 
mkdir folder/sub1 folder/sub2
touch folder/sub1/text.txt folder/sub1/image.png folder/sub2/conf.ini
mv folder/sub2 folder/sub1/sub11
mv folder/sub1/sub11/conf.ini folder/sub1/conf.ini
rm -r folder/sub1/sub11
rm folder/sub1/image.png
echo "Hello world !" > folder/sub1/text.txt 


The log files now contains the following logs :

29/09/2016-15:19:36 INFO Folder superviser started.
29/09/2016-15:20:06 INFO The folder folder/sub1 has been added.
29/09/2016-15:20:06 INFO The folder folder/sub2 has been added.
29/09/2016-15:20:32 INFO The file folder/sub2/conf.ini has been added.
29/09/2016-15:20:32 INFO The file folder/sub1/text.txt has been added.
29/09/2016-15:20:32 INFO The file folder/sub1/image.png has been added.
29/09/2016-15:20:50 INFO The folder folder/sub2 has been moved to folder/sub1/sub11.
29/09/2016-15:20:50 INFO The file folder/sub2/conf.ini has been moved to folder/sub1/sub11/conf.ini.
29/09/2016-15:21:20 INFO The file folder/sub1/sub11/conf.ini has been moved to folder/sub1/conf.ini.
29/09/2016-15:21:30 INFO The folder folder/sub1/sub11 has been deleted.
29/09/2016-15:22:06 INFO The file folder/sub1/image.png has been deleted.
29/09/2016-15:22:22 INFO The file folder/sub1/text.txt has been modified.
