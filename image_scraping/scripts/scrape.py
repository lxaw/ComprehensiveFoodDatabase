##################################
#
# Webscraping Images for Foods.
# Written by Lex Whalen (05/23/22)
# MIT License.
# 
# This program uses GoogleImages to 
# scrape images and store them.
#
##################################

# for scraping pages
from bs4 import BeautifulSoup
# for sleeping (can't DDOS!)
import time

# for http requests
import requests
# resize img
from PIL import Image
# regex
import re
# for get cpu count
from multiprocessing import cpu_count
# for threading
from threading import Thread
# locks
from threading import Lock

# mmap for file reading
import mmap

# dealing with dirs
import os

# Required headers to use BS4
kHEADERS = requests.utils.default_headers()
kEMAIL = "youremail@gmail.com"
kBROWSER = "Mozilla/5.0"
kHEADERS.update({
    'User-Agent':kBROWSER,
    'From':kEMAIL
})

# how large to save the icons
kICON_WIDTH = 150
kICON_HEIGHT = 150

# Parse the search query into a format 
# GoogleImages can understand.
# Example:
# input:
# "Almond Joy Pieces"
# output:
# "almond+AND+pieces"
def strFormatQuery(strQuery):
    """
    # INPUT:
    # String that is delimited by spaces.
    # Note that this function is not to accept
    # strings with spaces in the beginning or end.
    # OUTPUT:
    # Replaces single or continous spaces with one "+AND+"
    """
    # convert to lowercase
    strRes = strQuery.lower()

    # replace special characters
    #
    dictSpecialChars = {
        '&':'%26',
        '?':'%3F',
        '#':'%23'
    }

    # convert tabs to spaces
    strRes = re.sub("\t",' ',strRes)
    # convert commas to spaces
    strRes = re.sub(',',' ',strRes)

    # convert any spaces (single or multiple in a row)
    # to one "+AND+"
    strRes =re.sub(' +','+AND+',strRes)

    # convert any occurences of special chars to 
    # their GoogleImages equivalents
    for k,v in dictSpecialChars.items():
        strRes = strRes.replace(k,v)
    return strRes

# Given a formatted query (see strFormatQuery)
# create a GoogleImages formatted URL.
def strCreateUrlFromFormattedQuery(strFormattedQuery):
    # creates a url that GoogleImages can understand
    retStr = "https://www.google.com/search?q={}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiXt8DEr-n3AhXymeAKHRK1ASUQ_AUoAXoECAEQAw&biw=960&bih=871&dpr=1".format(strFormattedQuery)

    return retStr

# Get an image link from Google Images.
# Gets the first image available.
# Thus it performs no checks as to the accuracy of the image,
# or the licensing.
def strGetFirstImgLink(query):
    """
    Output: an image link.
    Input: a formated query string (see `strFormatQuery`)
    """
    # request the html page
    req = requests.get(query,headers = kHEADERS)

    # format it with bs4
    soup = BeautifulSoup(req.content,'html.parser')

    res = soup.select('img[src^=http]')
    if(len(res) != 0):
        return res[0]['src']
    else:
        # get the image from the website 
        return 

# Download an image given an image link.
#
def voidDownloadImgFromLink(strFilePath,strLink):
    # save to file

    with open(strFilePath,'wb') as f:
        f.write(requests.get(strLink).content)

# Resize an image.
# NOTE THAT THIS OVERWRITES THE IMAGE.
#
def voidResizeImgFile(strFilePath,intWidth,intHeight):
    img = Image.open(strFilePath).convert('RGB')
    img.thumbnail(size=(intWidth,intHeight))
    img.save(strFilePath,optimize=True,quality=50)


# Search a query and download the first image that appears.
# Note that this does not take into account
# the accuracy of the image or the licensing.
def voidSearchAndDownloadTopImg(strQuery,strFilePath):
    # prepare the query
    strFormattedQuery = strCreateUrlFromFormattedQuery(strFormatQuery(strQuery))

    strImgLink = strGetFirstImgLink(strFormattedQuery)

    voidDownloadImgFromLink(strFilePath,strImgLink)
    voidResizeImgFile(strFilePath,kICON_WIDTH,kICON_HEIGHT)

# Get the number of lines of a file.
# Note that here we only care about parsing individual lines,
# so we need to calculate line counts only.
# Source: https://stackoverflow.com/questions/845058/how-to-get-line-count-of-a-large-file-cheaply-in-python
# See Michael Bacon's solution: Brilliant!
def intGetLineCountFromFile(strFileName):
    f = open(strFileName,'rb')
    lines = 1
    buf_size = 1024 * 1024
    read_f = f.raw.read

    buf = read_f(buf_size)
    while buf:
        lines += buf.count(b'\n')
        buf = read_f(buf_size)
    return lines

# Parse file into parts.
# Returns list.
def listParseFile(strFileName,intDivisions):
    # Get the number of lines
    intLineCount = intGetLineCountFromFile(strFileName)

    # the number of  divisions for each regular part
    # meaning, if there is a remainder, we put the remainder
    # completely in the last section.
    intRegularSectionLineWidth = intLineCount // intDivisions
    # last section line count is 
    # intRegularSectionLineWidth + Remainder
    # No need to store remainder until calculation.

    # create the number of lists you need
    #
    listRet = [[]] * intDivisions
    # populate make the lists of the size you 
    # need
    for i in range(0,intDivisions):
        if(i == intDivisions - 1):
            listRet[i] = [0]*(
                intRegularSectionLineWidth + (intLineCount % intDivisions)
            )
        else:
            listRet[i] = [0]*intRegularSectionLineWidth
    
    # now populate the lists
    # with text
    #
    # For indexing listRet's inner lists
    intListIndex = 0
    # for indexing within list's of listRet
    intListInnerIndex = 0

    with open(strFileName) as f:
        for line in f:
            listRet[intListIndex][intListInnerIndex] = line

            intListInnerIndex += 1
            if (intListInnerIndex!= 0) and (intListInnerIndex % intRegularSectionLineWidth == 0):
                if intListIndex != (intDivisions - 1):
                    # just go to next list
                    intListIndex += 1
                    # always need to reset intListInnerIndex to 0, since
                    # now we go to a new list.
                    intListInnerIndex = 0
    return listRet

# removes non alphanumeric characters
#
def strRemoveNonAlphaNumeric(strName):
    return re.sub('[^0-9a-zA-Z]','',strName)

# BAD DESIGN: Global Variable to count how many requests made.
# At moment (05/19/22) don't know better option.
# When you hit >= kMAX_REQUESTS_AT_TIME, pause the threads.
kMAX_REQUESTS_AT_TIME = 200
CURRENT_REQUEST_COUNT = 0
kGLOBAL_REQUEST_COUNT_LOCK = Lock()

# performs processing for worker process
# Downloads the imgs from google
def voidWorkerProcess(strDirName,listFragment,lockLock):
    # Inputs:
    # strDirName: directory name to save images to
    # listFragment: the fragment of the list that the current thread is to process
    # lockLock: the mutex shared by threads

    for i in range(0,len(listFragment)):
        global CURRENT_REQUEST_COUNT
        global kMAX_REQUESTS_AT_TIME

        # find the correct file directory
        strSubDirName,strFoodName = listFragment[i].split('\t')
        strSubDirName = strRemoveNonAlphaNumeric(strSubDirName)
        strFoodName = strRemoveNonAlphaNumeric(strFoodName)
        strPath = os.path.join(strDirName,strSubDirName,strFoodName + '.jpeg')

        if not os.path.exists(strPath):
            try:

                lockLock.acquire()
                local_counter = CURRENT_REQUEST_COUNT
                local_counter += 1
                CURRENT_REQUEST_COUNT = local_counter
                # if greater, sleep the thread
                if(CURRENT_REQUEST_COUNT >= kMAX_REQUESTS_AT_TIME):
                    time.sleep(1.0)
                    # then reset to 0
                    CURRENT_REQUEST_COUNT = 0
                lockLock.release()
                # create the file if not exists
                #
                voidSearchAndDownloadTopImg(listFragment[i],strPath)

            except Exception as e:
                print("ERROR WITH {}".format(listFragment[i]))
                print("Error:\n{}".format(e))
                pass

# create the directories to store images in
#
def voidCreateDirectories(strTextFilePath,strBaseDirPath):
    with open(strTextFilePath,'r') as f:
        # get a list of all the directories in the directory
        listPrexistingDirs = os.listdir(strBaseDirPath)
        setDirNames = set()
        for line in f:
            strNewDirName = strRemoveNonAlphaNumeric(line.split('\t')[0])
            # check if the directory is present
            # if not, make
            if strNewDirName in listPrexistingDirs:
                continue
            else:
                # create the dir
                strNewDirPath = os.path.join(strBaseDirPath,strNewDirName)
                setDirNames.add(strNewDirPath)
    # now we have all the unique dir names, we make the dirs that are not 
    # present yet
    for e in setDirNames:
        if e in listPrexistingDirs:
            continue
        else:
            if not os.path.exists(e):
                os.mkdir(e)

# Downloads imgs using threads.
# The number of threads depends on the number of cores.
#
def voidThreadedProcessing(strTextFileName,strOutDirFolder,intNumThreads,lockLock):
    # Inputs:
    # strTextFileName: source text file for scraping images
    # strOutDirFolder: the directory to save images to
    # intNumThreads: the number of threads to perform work
    # lockLock: the mutex
    listFileParts = listParseFile(strTextFileName,intNumThreads)

    listThreads = [ Thread(target=voidWorkerProcess,args = (strOutDirFolder,listFileParts[i],lockLock)) for i in range(0,intNumThreads) ]

    for i in range(0,intNumThreads):
        listThreads[i].start()

    for i in range(0,intNumThreads):
        listThreads[i].join()

if __name__ == "__main__":
    kSRC_FILE_PATH = 'src_data/usda_no_branded.txt'
    kOUT_DIR = 'imgs/usda_non_branded'

    # first create the dirs to store the images
    voidCreateDirectories(kSRC_FILE_PATH,kOUT_DIR)

    kNUM_CORES =cpu_count()
    # print("STARTING PROCESSING WITH {} THREADS".format(kNUM_CORES))
    voidThreadedProcessing(strTextFileName =kSRC_FILE_PATH,
                        strOutDirFolder=kOUT_DIR,
                        intNumThreads = kNUM_CORES,lockLock = kGLOBAL_REQUEST_COUNT_LOCK)
