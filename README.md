# Script for Fixing Timestamps

## Introduction
This repository contains scripts that process the lena.cha and sparse code cha files in pairs to revert the modified timestamps in the sparse code cha file to their original states as in the lena cha file.  
The core component of the code calls difflib (similar to diff command in shell) to compute the line to line difference among the timestamps across the file, and attempts to recognize the changes.

## Usage
fill_missing_line.py is the only actual script that does the work, but it calls the restore_timestamps method from the timestamp_revert_brute.py in order to function.  
Change line 5 and 6 of the fill_missing_line.py script to modify the location of folders that contain the lena files and sparse code files. Those two can be in different folders. Modify line 9 to specify the output folder, which has to be manually created beforehand.  
Then run:
```
python3 fill_missing_line.py
```
Python3 is preferred although python2 should also work.