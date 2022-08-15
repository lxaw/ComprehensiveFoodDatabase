#######################
#
# Print the total file count of a directory.
# Used to determine if the program was able to download
# the correct number of image files.
#

import sys
import os

#####
# Return the number of files in a directory.
#
def intFileCount(strPath):
    intCount = 0
    listDirs = os.listdir(strPath)
    for dir in listDirs:
        strDirPath = os.path.join(strPath,dir)
        intCount += len(os.listdir(strDirPath))

    return intCount

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: `python file_count.py [IMAGE SOURCE DIRECTORY PATH]`")
        exit()
    
    print('total count: {} files'.format(intFileCount(sys.argv[1])))
