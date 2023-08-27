# okay so to finalize this we need to set an input field and make it a function
# we need to crosscheck the districts with the json data
#and if we're feeling kind we can make an interactive map?
import sys
import os

def is_path_creatable(pathname: str) -> bool:
    '''
    `True` if the current user has sufficient permissions to create the passed
    pathname; `False` otherwise.
    '''
    # Parent directory of the passed path. If empty, we substitute the current
    # working directory (CWD) instead.
    dirname = os.path.dirname(pathname) or os.getcwd()
    return os.access(dirname, os.W_OK)

def is_path_exists_or_creatable(pathname: str) -> bool:
    '''
    `True` if the passed pathname is a valid pathname for the current OS _and_
    either currently exists or is hypothetically creatable; `False` otherwise.

    This function is guaranteed to _never_ raise exceptions.
    '''
    try:
        # To prevent "os" module calls from raising undesirable exceptions on
        # invalid pathnames, is_pathname_valid() is explicitly called first.
        return is_pathname_valid(pathname) and (
            os.path.exists(pathname) or is_path_creatable(pathname))
    # Report failure on non-fatal filesystem complaints (e.g., connection
    # timeouts, permissions issues) implying this path to be inaccessible. All
    # other exceptions are unrelated fatal issues and should not be caught here.
    except OSError:
        return False






endpt=input("enter the full path of the file you'd like to create (i.e C:/USER/Desktop/sheet.xlsx")
while is_path_creatable(endpt)==False or endpt[len(endpt)-5:len(endpt)] != ".xlsx":
    print("that aint a valid path")
    endpt=input("enter the full path of the file you'd like to create (i.e C:/USER/Desktop/sheet.xlsx")


if os.path.exists(endpt):
    print("This file already exists, running this program will overwrite any manual changes you've added to the previous version")
    print("If the path you listed is your master document we strongly suggest you cancel the program")
    finalChance=input("If you wish to continue, hit enter. Otherwise hit any other key")
else:
    finalChance=""

if finalChance=="":
    Boroughs=["X","B","M","R","Q"]
    BoroughInquiry=input("Which Borough Would you like to Scrape?\n enter one of the following: \n Q for Queens \n B for Brooklyn\n X for The Bronx\n R for Staten Island \n M for Manhattan\n")
    
    
    while BoroughInquiry not in Boroughs:
        BoroughInquiry=input("Please enter a valid borough, the options are \n Q for Queens \n B for Brooklyn\n X for The Bronx\n R for Staten Island \n M for Manhattan\n")
        
    import re
    import requests
    from bs4 import BeautifulSoup
    import openpyxl
    import numpy as np
    import pandas as pd
    import string
    idxs=range(1000)
    baseID='000'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'}

    URL=r"https://www.nycgovparks.org/parks/" + BoroughInquiry
    nameList=["junk"]
    border="=============================================================="
    flag1="Viewers\n"+border+"\n\n"
    flag2="\n"+border+"\n\n-->"
    suffixes= list(" " + string.ascii_uppercase)

    jsonData=pd.read_json(r'https://data.cityofnewyork.us/resource/ve3w-z72j.json')

    geom_list=jsonData['the_geom']



    for n in idxs:
       
            suffixcheck=1
            for n2 in suffixes:
                    if suffixcheck==1:
                        tempID=int(len(baseID)-len(str(n)))*"0"+str(n)
                        tempURL=URL+tempID+n2
                        response = requests.head(tempURL,headers=headers)
                        print(BoroughInquiry + tempID+n2)
                        if response.status_code!=404:
                            
                            suffixcheck=1
                            page = requests.get(tempURL, headers=headers)
                            
                            pageTxt=BeautifulSoup(page.content,"html.parser")
                            strPage=str(pageTxt)
                            goodStuff = pageTxt.find(id="park_more_details")

                            if re.search('<strong>Property Type:</strong>\n\t\t(.*)\n\t\t</p>',str(goodStuff))!="Parkway":
                            
                                location_element = pageTxt.find_all(class_="park_location")

                                tempXstreet=re.search('margin-bottom: 0;">(.*)</p>',str(location_element))
                            
                                title_element = pageTxt.find_all(class_="park_name_title")

                                tempName=re.search('<h1 class="park_name_title">(.*)</h1>',str(title_element))

                                if strPage.find(flag1) > 0:
                                    tempFact=strPage[strPage.find(flag1)+len(flag1):strPage.find(flag2)-2]
                                else:
                                    tempFact='N/A'

                                tempZIP=re.search('Zip Code:</strong>(.*)<br/>', str(goodStuff))

                                tempArea=re.search('<strong>Acreage:</strong>\n\t\t(.*)\n\t\t\t\t<br/>\n<strong>', str(goodStuff))
                                
                                tempType=re.search('<strong>Property Type:</strong>\n\t\t(.*)\n\t\t</p>',str(goodStuff))

                                tempDistrict=re.search('<strong>Council Member:</strong>\n<a href="http://council.nyc.gov/d(.*)/html/members/home.shtml">',str(goodStuff))
                                
                            
                                tempLoc=re.search("var oldGMapsString = '(.*)';",strPage)
                                    

                                if hasattr(tempName,'group'):
                                    
                                    if "junk" in nameList:
                                        nameList[0]=tempName.group(1)
                                    else:
                                        nameList.append(tempName.group(1))
                                
                                        
                                    if len(location_element) > 0:
                                        finalXstreet=str(tempXstreet.group(1))
                                    else:
                                        finalXstreet='none provided'


                                    if hasattr(tempZIP,'group'):
                                        finalZIP= tempZIP.group(1)
                                    else:
                                        finalZIP='N/A'

                                    if hasattr(tempArea,'group'):
                                        finalArea=float(tempArea.group(1))
                                    else:
                                        finalArea= 'N/A'
                                    if hasattr(tempType,'group'):
                                        finalType=tempType.group(1)
                                    else:
                                        finalType='N/A'

                                        
                                    if hasattr(tempDistrict,'group'):
                                        finalDistrict=int(tempDistrict.group(1))
                                    else:
                                        finalDistrict='N/A'
                                    if hasattr(tempLoc,'group'):
                                        finalLoc="https://www.google.com/maps/search/"+tempLoc.group(1)
                                        finalLat=tempLoc.group(1).split(",")[0]
                                        finalLong=tempLoc.group(1).split(",")[1]
                                    else:
                                        tempLat=re.search('var latitude = "(.*)";var longitude',strPage)
                                        tempLong=re.search('var longitude = "(.*)";var signName',strPage)

                                        if not hasattr(tempLat,'group') or tempLat.group(1)=="" or tempLong.group(1)=="" :
                                            mapPage = requests.get(tempURL+"/map", headers=headers)
                                            mapPageTxt=BeautifulSoup(mapPage.content,"html.parser")
                                            mapStrPage=str(mapPageTxt)
                                            tempLat=re.search('var latitude = "(.*)";var longitude',mapStrPage)
                                            tempLong=re.search('var longitude = "(.*)";var signName',mapStrPage)
                                            finalLat=tempLat.group(1)
                                            finalLong=tempLong.group(1)
                                            if finalLat=="" or finalLong=="":
                                               tempSWLat=re.search('var swLat = "(.*)";var swLong',mapStrPage)
                                               tempSWLong=re.search('var swLong = "(.*)";var neLat',mapStrPage)
                                               tempNELat=re.search('var neLat = "(.*)";var neLong',mapStrPage)
                                               tempNELong=re.search('var neLong = "(.*)";</script>',mapStrPage)
                                               if tempSWLat.group(1)!="" or tempNELat.group(1)!="" or tempSWLong.group(1)!="" or tempNELong.group(1)!="":
                                              
                                                       finalLat=str((float(tempSWLat.group(1))+float(tempNELat.group(1)))/2)
                                                       finalLong=str((float(tempSWLong.group(1))+float(tempNELong.group(1)))/2)
                                                       finalLoc="https://www.google.com/maps/search/"+finalLat+","+finalLong

                                               else:
                                                    finalLoc="none provided"
                                            else:
                                                 finalLoc="https://www.google.com/maps/search/"+finalLat+","+finalLong 
                                        else:
                                                finalLat=tempLat.group(1)
                                                finalLong=tempLong.group(1)
                                                finalLoc="https://www.google.com/maps/search/"+finalLat+","+finalLong

                                    

                                    tempRow=np.asarray([finalXstreet,finalLoc,finalZIP,finalArea,finalDistrict,finalType,tempFact,strPage.find('"park_facilities_list_text">Public Restrooms')>0,strPage.find('"park_facilities_list_text">Dog-friendly Areas') > 0,strPage.find('"park_facilities_list_text">Outdoor Pools') > 0,strPage.find('"park_facilities_list_text">Indoor Pools') > 0,BoroughInquiry + tempID+n2],dtype=object)

                                    #if we have a valid district and set of coordinates. Should consider a subfunction that verifies an existing sheet.
                                    if 'outputArray' in locals():
                                        outputArray=np.vstack([outputArray,tempRow],dtype=object)
                                    else:
                                        outputArray=tempRow
                        else:
                            suffixcheck=0
    attributes=["Cross Streets","Maps Link","ZIP","Area","District","Type","Fun Fact","Has Restroom?","Has Dogrun?","Has Outdoor Pool?","Has Indoor Pool?","Park Code"]

    ParksData=pd.DataFrame(outputArray,index=nameList,columns=attributes)

    ParksData.to_excel(endpt)


