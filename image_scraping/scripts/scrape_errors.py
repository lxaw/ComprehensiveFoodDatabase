##################################
#
# Webscraping Images for Foods.
# Written by Lex Whalen (05/23/22)
# MIT License.
# 
# This program reads the error_log file
# created when running "scrape.py".
# This error_log is created by running
# "python3 scrape.py > error_log.txt"
#
##################################

# for getting the images
from scrape import voidSearchAndDownloadTopImg,strSlugName,strFormatQuery
# for pattern recog
import re
# to make sure we dont get blocked
import time

# Find all the missed entries from error_log.
# Return them as a list.
def listGetMissedFiles(strFileName):
    # All errors begin with
    # "ERROR WITH "
    # and then the rest is the
    # name of the entry.

    listRet = []

    pattern = re.compile(r'(?<=^ERROR WITH ).*')
    with open(strFileName) as f:
        for line in f:
            res = re.search(pattern,line)
            if res != None:
                listRet.append(res.group(0))

    return listRet

# from bs4 import BeautifulSoup
# import requests
# listEntries = listGetMissedFiles("examples/error_log.txt")
# test =strFormatQuery(listEntries[0])


# # Required headers to use BS4
# kHEADERS = requests.utils.default_headers()
# kEMAIL = "whalenlex@gmail.com"
# kBROWSER = "Mozilla/5.0"
# kHEADERS.update({
#     'User-Agent':kBROWSER,
#     'From':kEMAIL
# })

# query = "https://www.google.com/search?q={}&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiXt8DEr-n3AhXymeAKHRK1ASUQ_AUoAXoECAEQAw&biw=960&bih=871&dpr=1".format(test)
# print("QUERY:\n{}".format(query))
# # how large to save the icons
# kICON_WIDTH = 150
# kICON_HEIGHT = 150

# req = requests.get(query,headers = kHEADERS)
# soup = BeautifulSoup(req.content,'html.parser')
# imgs = soup.find_all('a')
# for link in imgs:
#     print(link)

# Save all the missed entries to a folder
# 
def voidGetAllListEntriesToFolder(strDirName,listEntries):
    intCount = 0
    for strEntry in listEntries:
        # create the file path
        strSlug = strSlugName(strEntry)
        strFileName = strDirName + "/" + strSlug + ".jpeg"

        try:
            voidSearchAndDownloadTopImg(strEntry,strFileName)
            intCount +=1
            if intCount == 50:
                time.sleep(1)
                intCount = 0

        except Exception as e:
            print("ERROR WITH {}".format(strEntry))
            print("Error:\n{}".format(e))
            pass
        
if __name__ == "__main__":
    listEntries = listGetMissedFiles("examples/error_log.txt")
    voidGetAllListEntriesToFolder("test",listEntries)
