import re
import pandas as pd
from bs4 import BeautifulSoup as bs
import time

from urllib.request import urlopen, Request

# base url for alphabetical listings
# all other urls append the letter of alphabet
# ie: [URL_ALPHA_BASE] + "a" gives `a` starting restaurants
URL_ALPHA_BASE= "https://www.menuwithnutrition.com/restaurant/"

# url to provide base for restaurant searches
URL_REST_BASE = "https://www.menuwithnutrition.com/"

# headers for query
HEADERS = {"User-Agent":"Mozilla/5.0"}

def getSoup(strUrl):
    # returns the soup for htmlparser
    r = Request(strUrl, headers = HEADERS)
    res = urlopen(r).read()
    soup = bs(res,'html.parser')

    return soup

def listGetRestUrlsFromBaseAlphaPage():
    # Inputs: a url of a page that is contains restaurants starting with letter
    # Returns: list of urls from a page containing the brands of some letter

    listRet = []

    # loop thru alphabet
    alphabet = [(chr(ord('a')+i)) for i in range(26)]
    for letter in alphabet:
        try:
            strCurrentUrl = URL_ALPHA_BASE + letter
            soup = getSoup(strCurrentUrl)
            # the pattern is thus:
            # look for a tags with href = ".*-menu-nutrient"
            # [1:] because do not want leading '/'
            hrefs = [URL_REST_BASE + i.attrs['href'][1:] for i in soup.find_all("a",attrs={"href":re.compile(r".*-menu-nutrition")})]
            listRet += hrefs
        except Exception as e:
            print('error at letter `{}`: \n{}'.format(letter,e))
            continue

    return listRet

def listGetFoodUrlsFromRestPage(strUrl):
    # gets the food urls from each rest page
    # ie: https://www.menuwithnutrition.com/aandw-restaurant-menu-nutrition/ --> get all foods from there

    # name to check to ensure that we are getting only restaurant urls
    strCheckName= strUrl.replace(URL_REST_BASE,"")

    soup = getSoup(strUrl)

    # urls are format: `[strUrl] + /[FOOD_NAME]-[SOME NUMBER]`
    # [1:] because do not want leading '/'
    hrefs = []
    for i in soup.find_all("a",{"class":"item-a-cover"}):
        try:
            href = i.attrs['href'][1:]
            if strCheckName in href:
                hrefs.append(URL_REST_BASE + href)
        except Exception as e:
            print('listGetFoodUrlsFromRestPage\nerror with: {}\n{}'.format(i,e))
            continue


    return hrefs

def strGetRestNameFromFoodUrl(strUrl):
    strRestName = " ".join(strUrl[:-1].split('/')[-2].replace('-menu-nutrition','').split('-'))
    return strRestName

def dictGetFoodNutrition(strUrl,strRestName):
    # returns nutrition info from url
    soup = getSoup(strUrl)

    # get name of item
    strItemName = " ".join(strUrl[:-1].split('/')[-1].split('-')[0:-1])


    dictNutrients = {}
    dictNutrients['Restaurant Name'] = strRestName
    dictNutrients['Food Name'] = strItemName
    # first get totals
    for trNutritionItemWrap in soup.find_all("tr",{"class":"nutrition-item-wrap"}):
        strNutrientName = trNutritionItemWrap.find('td',{'class':'nutrition-item-name'}).text
        strNutrientAmount = trNutritionItemWrap.find('span',{'class':'calculator-multiple-num'}).text
        strNutrientUnit = trNutritionItemWrap.find('span',{'class':'nutrition-unit'}).text
        
        # put into dictionary
        dictNutrients[strNutrientName+" Amount"] = strNutrientAmount
        dictNutrients[strNutrientName+" Unit"] = strNutrientUnit

    # then get the data under
    for trNutritionContentSingle in soup.find_all("tr",{"class":"nutrition-content-single"}):
        strNutrientName = trNutritionContentSingle.find('td',{'class':'nutrition-single-name'}).text
        strNutrientAmount = trNutritionContentSingle.find('span',{'class':'calculator-multiple-num'}).text
        strNutrientUnit = trNutritionContentSingle.find('span',{'class':'nutrition-unit'}).text

        # put into dict
        dictNutrients[strNutrientName+" Amount"] = strNutrientAmount
        dictNutrients[strNutrientName+" Unit"] = strNutrientUnit

    # print(dictNutrients)
    
    return dictNutrients

def voidDictsToCsv(listDicts):
    # takes a list of all dicts of all foods and makes a csv file out of them

    # init a basic dataframe from first dictionary
    df = pd.DataFrame(columns = ['Restaurant Name','Food Name'])

    for dictFood in listDicts:
        for k in dictFood.keys():
            if k not in df:
                # add
                df[k] = ''
            # add data
            df = df.append(dictFood,ignore_index=True)

    df.to_csv('out.csv')

if __name__ == "__main__":
    # get all restaurant urls
    listRestUrls = listGetRestUrlsFromBaseAlphaPage()
    # get all foods from restuarant
    listFoodItemUrls = []
    for url in listRestUrls:
        try:
            listFoodItemUrls += listGetFoodUrlsFromRestPage(url)
        except Exception as e:
            print('error with `{}`: \n{}'.format(url,e))
            print()
            continue
    # delete unneeded list
    del listRestUrls

    listDictFoodData = []
    counter = 0
    for url in listFoodItemUrls:
        try:
            strRestName = strGetRestNameFromFoodUrl(url)
            listDictFoodData.append(dictGetFoodNutrition(url,strRestName))
            counter +=1
            if counter == 60:
                time.sleep(3)
                counter = 0
        
        except Exception as e:
            print('error with `{}`: \n{}'.format(url,e))
            print()
            continue
    # delete unneeded list
    del listFoodItemUrls
    # create csv
    voidDictsToCsv(listDictFoodData)


