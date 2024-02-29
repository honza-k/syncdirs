# Veeam Homework
## Directory synchronization

### Test Task
Please implement a program that synchronizes two folders: source and replica. The
program should maintain a full, identical copy of source folder at replica folder.
Solve the test task by writing a program in one of these programming languages:
* Python
* C/C++
* C#

- Synchronization must be one-way: after the synchronization content of the
replica folder should be modified to exactly match content of the source
folder;
- Synchronization should be performed periodically.
- File creation/copying/removal operations should be logged to a file and to the
console output;
- Folder paths, synchronization interval and log file path should be provided
using the command line arguments;
- It is undesirable to use third-party libraries that implement folder
synchronization;
- It is allowed (and recommended) to use external libraries implementing other
well-known algorithms. For example, there is no point in implementing yet
another function that calculates MD5 if you need it for the task – it is
perfectly acceptable to use a third-party (or built-in) library.

----------------------------
### Notes to chosen solution:

- Developed and tested using **Python 3.12.0**
- Simple recursion for traversing both source and replica directory has been used.
- Script doesn't care of space on dst/replica device.
- Only regular files and directories are supported.
- Script doesn't handle ownership and access rights.

### Usage:

Following example replicates directory `source_data` into directory `replica`
with period 120 seconds and it logs messages into `syncdirs.log` log file.

`python -m syncdirs -s source_data -r replica -i 120 -l syncdirs.log`

