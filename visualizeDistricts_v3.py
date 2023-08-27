import pandas as pd
import geopandas as gpd
from shapely import buffer
from shapely import geometry
from shapely import Polygon
from shapely import LineString
from shapely import unary_union
import matplotlib.pyplot as plt
import numpy as np; np.random.seed(1)
import webbrowser
import os
from shapely.ops import unary_union
import folium
import string
import re
from shapely import Point
import math
from shapely import multipolygons
##room for improvement
## 1) implement some kind of search/filtering capability
## 2) figure out how to add a third layer (didn't display last time and crashed layer selecter)

pathname=input("Enter the path of the file generated by new_scraper.py\n")
##
##while not os.path.exists(pathname):
##    print("that wasn't a valid path")
##    pathame=input("Enter the path of the file generated by new_scraper.py\n")

BiD=input("Which Borough Would you like to Visualize?\n enter one of the following: \n Q for Queens \n B for Brooklyn\n X for The Bronx\n R for Staten Island \n M for Manhattan\n")
    
Boroughs=["X","B","M","R","Q"]
while BiD not in Boroughs:
        BiD=input("Please enter a valid borough, the options are \n Q for Queens \n B for Brooklyn\n X for The Bronx\n R for Staten Island \n M for Manhattan\n")

SaveTo=input("Enter the path of the folder where you'd like the result to be saved")

##while not os.path.isdir(SaveTo):
##    print("please enter a valid folder")
##    SaveTo=input("Enter the path of the folder where you'd like the result to be saved")

Districts=pd.read_json(r'https://data.cityofnewyork.us/resource/ve3w-z72j.json')

DistrictNums={"Q" : [19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34],"M" : [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "R": [49,50,51], "X": [8,11, 12, 13, 14, 15, 16, 17, 18],"B": [33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50]}
districtShapes=list()
districtID=list()

for n in range(len(Districts)):
    if Districts["coun_dist"][n] in DistrictNums[BiD]:
        for n2 in range(len(Districts["the_geom"][n]["coordinates"])):
            polygon1=Polygon(Districts["the_geom"][n]["coordinates"][n2][0])
            districtID.append(Districts["coun_dist"][n])
            districtShapes.append(polygon1)

d={'District':districtID}
df = pd.DataFrame(d)
gs=gpd.GeoSeries(data=districtShapes)
gdfDistricts = gpd.GeoDataFrame(df, geometry=gs,crs=4326)


mapa=gdfDistricts.explore(style_kwds={'color':'black','weight':3,'fillColor':'red','fillOpacity':0.4},highlight_kwds=dict(fillOpacity='0.2'),name="Districts")




            
Parks=pd.read_json(r'https://data.cityofnewyork.us/resource/knjr-pgub.json?borough='+BiD)
manualdata=pd.read_excel(pathname)
parkShapes=list()
badIDXs=list(manualdata["Park Code"])
codeIDXs=list()
for n in range(len(badIDXs)):
    codeIDXs.append(badIDXs[n].replace(" ",""))

parkNames=list()
Xstreets=list()
MapsLink=list()
Area=list()
parkDistricts=list()
suffixes= list(string.ascii_uppercase)
geoDistricts=list()
dogRun=list()
restRoom=list()
for n in range(len(Parks)):
    
    for n2 in range(len(Parks["the_geom"][n]["coordinates"])):
        
        Parks["the_geom"][n]["coordinates"][n2]=Polygon(Parks["the_geom"][n]["coordinates"][n2][0])
        
    
    multiPark=multipolygons(Parks["the_geom"][n]["coordinates"])
    for n2 in range(len(Parks["the_geom"][n]["coordinates"])):
        Parks["the_geom"][n]["coordinates"][n2]=buffer(Parks["the_geom"][n]["coordinates"][n2],.00005)
        
    parkShapes.append(unary_union(Parks["the_geom"][n]["coordinates"]))
    
    if Parks["gispropnum"][n] + " " in codeIDXs or Parks["gispropnum"][n] in codeIDXs:
    
        
        xlLoc=codeIDXs.index(Parks["gispropnum"][n])
        
            

        
        parkNames.append(manualdata["Park Name"][xlLoc])
        Xstreets.append(manualdata["Cross Streets"][xlLoc])
        MapsLink.append("<a href='" + manualdata["Maps Link"][xlLoc] + "' target='blank'>Google Maps Link</a>")
        Area.append(float(manualdata["Area"][xlLoc]))
        parkDistricts.append(str(manualdata["District*"][xlLoc]))
        dogRun.append(manualdata["Has Dogrun?"][xlLoc])
        restRoom.append(manualdata["Has Restroom?"][xlLoc])
    else:
        parkNames.append(Parks["sitename"][n])
        Xstreets.append(Parks["location"][n])
        MapsLink.append('')
        if Parks["acres"][n] == '':
            Area.append(0)
        else:
            Area.append(float(Parks["acres"][n]))
        parkDistricts.append(str(Parks["councildistrict"][n]))
        dogRun.append(False)
        restRoom.append(False)
    tempGeoDist=list()
    for n3 in range(len(gdfDistricts)):
        if multiPark.intersects(gdfDistricts["geometry"][n3]):
            tempGeoDist.append(gdfDistricts["District"][n3])
    if len(tempGeoDist) > 1:
        geoDistricts.append(0)
    elif bool(tempGeoDist)==False:
        geoDistricts.append(0)
    else:
        geoDistricts.append(tempGeoDist[0])
            
parkList=set(Parks["propname"])
uniParkShapes=list()
uniParkNames=list()
uniXstreets=list()
uniMapsLink=list()
uniArea=list()
uniParkDistrict=list()
uniRestRoom=list()
uniDogRun=list()
uniGeoDist=list()
for n in parkList:
        FianceS=list()
        for n2 in [ind for ind, ele in enumerate(list(Parks["propname"])) if ele == n]:

                for n3 in range(len(Parks["the_geom"][n2]['coordinates'])):
                        
                        

                        FianceS.append(Parks["the_geom"][n2]["coordinates"][n3])

        uniParkShapes.append(unary_union(FianceS))
        uniParkNames.append(n)
        uniXstreets.append(Xstreets[n2])
        uniMapsLink.append(MapsLink[n2])
        uniArea.append(Area[n2])
        uniParkDistrict.append(parkDistricts[n2])
        uniRestRoom.append(restRoom[n2])
        uniDogRun.append(dogRun[n2])
        uniGeoDist.append(geoDistricts[n2])
        



    
##    tempParkShapes=list()
##    for n2 in range(len(Parks["the_geom"][n]["coordinates"])):
##        ParkPoly=Polygon(Parks["the_geom"][n]["coordinates"][n2][0])
##        parkShapes.append(ParkPoly)
##    
##        if Parks["gispropnum"][n] + " " in codeIDXs or Parks["gispropnum"][n] in codeIDXs:
##        
##            
##            xlLoc=codeIDXs.index(Parks["gispropnum"][n])
##            
##                
##
##            
##            parkNames.append(manualdata["Park Name"][xlLoc])
##            Xstreets.append(manualdata["Cross Streets"][xlLoc])
##            MapsLink.append("<a href='" + manualdata["Maps Link"][xlLoc] + "' target='blank'>Google Maps Link</a>")
##            Area.append(float(manualdata["Area"][xlLoc]))
##            parkDistricts.append(str(manualdata["District"][xlLoc]))
##            dogRun.append(manualdata["Has Dogrun?"][xlLoc])
##            restRoom.append(manualdata["Has Restroom?"][xlLoc])
##        else:
##            parkNames.append(Parks["sitename"][n])
##            Xstreets.append(Parks["location"][n])
##            MapsLink.append('')
##            Area.append(float(Parks["acres"][n]))
##            parkDistricts.append(str(Parks["councildistrict"][n]))
##            dogRun.append(False)
##            restRoom.append(False)
##        tempGeoDist=list()
##        for n3 in range(len(gdfDistricts)):
##            if ParkPoly.intersects(gdfDistricts["geometry"][n3]):
##                tempGeoDist.append(gdfDistricts["District"][n3])
##        if len(tempGeoDist) > 1:
##            geoDistricts.append(0)
##        elif bool(tempGeoDist)==False:
##            geoDistricts.append(0)
##        else:
##            geoDistricts.append(tempGeoDist[0])
##            
##

    ##things to add
    ## search functionality?
    ## data on whether a park contains a dog run or bathroom etc and a way to highlight those parks
   
    

dotPts = list(set(codeIDXs) - set(Parks["gispropnum"]))

for n in dotPts:
    if hasattr(re.search('https://www.google.com/maps/search/(.*)',manualdata["Maps Link"][codeIDXs.index(n)]),'group'):
        strPt=re.search('https://www.google.com/maps/search/(.*)',manualdata["Maps Link"][codeIDXs.index(n)]).group(1).split(',')
        if manualdata["Area"][codeIDXs.index(n)] > 0 and manualdata["Type"][codeIDXs.index(n)]!='Parkway' :
            tempBuff=math.sqrt(manualdata["Area"][codeIDXs.index(n)])* 0.00053137662634174832

            
        else:
            tempBuff=.0005
        uniParkShapes.append(Point([float(strPt[1]),float(strPt[0])]).buffer(tempBuff))

        
    uniParkNames.append(manualdata["Park Name"][codeIDXs.index(n)])
    uniXstreets.append(manualdata["Cross Streets"][codeIDXs.index(n)])
    uniMapsLink.append("<a href='" + manualdata["Maps Link"][codeIDXs.index(n)] + "' target='blank'>Google Maps Link</a>")
    uniArea.append(float(manualdata["Area"][codeIDXs.index(n)]))
    uniParkDistrict.append(str(manualdata["District*"][codeIDXs.index(n)]))
    uniDogRun.append(manualdata["Has Dogrun?"][codeIDXs.index(n)])
    uniRestRoom.append(manualdata["Has Restroom?"][codeIDXs.index(n)])

    if True in list(gs.contains(Point([float(strPt[1]),float(strPt[0])]))):
        uniGeoDist.append(gdfDistricts["District"][list(gs.contains(Point([float(strPt[1]),float(strPt[0])]))).index(True)])
    else:
        uniGeoDist.append(0)
    


    


d2={'Park Name':uniParkNames,'Reported District': uniParkDistrict,"Geo-Verified District":uniGeoDist,'Maps Link':uniMapsLink,'Cross Streets':uniXstreets,"Area":uniArea,"Has Dog-Run?": uniDogRun,"Has Restroom?": uniRestRoom}     
                  
df2 = pd.DataFrame(d2)

gs2=gpd.GeoSeries(data=uniParkShapes)
gdfParks = gpd.GeoDataFrame(df2, geometry=gs2,crs=4326)
mapa=gdfParks.explore(m=mapa,popup=True,cmap="Set1",tooltip = False,style_kwds=dict(color="green",fillcolor="green",fillOpacity='0.6'),highlight_kwds=dict(fillOpacity='.2'),name="Parks")
#folium.LayerControl().add_to(mapa)


dogRunLayer=gdfParks.iloc[[i for i, x in enumerate(list(gdfParks["Has Dog-Run?"])) if x]]

mapa=dogRunLayer.explore(m=mapa,popup=True,cmap="Set1",tooltip = False,style_kwds=dict(stroke=False,fillcolor="Blue",fillOpacity='0.5'),highlight_kwds=dict(fillOpacity='.2'),name="Has Dogrun?")
#folium.LayerControl().add_to(mapa)  # use folium to add layer control
restRoomLayer=gdfParks.iloc[[i for i, x in enumerate(list(gdfParks["Has Restroom?"])) if x]]


mapa=restRoomLayer.explore(m=mapa,popup=True,cmap="Set1",tooltip = False,style_kwds=dict(stroke=False,color="Yellow",fillcolor="Yellow",fillOpacity='0.5'),highlight_kwds=dict(fillOpacity='.2'),name="Has Restroom??")

#folium.LayerControl().add_to(mapa)  # use folium to add layer control
### multiple layers can be added effectively
### however the explore function doesnt recognize when you add a map unto an existing map
### and consequently adds a new layer conrol element even tho one was created for the last map
### thus all but the last layer control must be deleted in order to display all layers properly








mapa.save(SaveTo + "/" + BiD +'_ParksMaps.html')
webbrowser.open(SaveTo + "/" + BiD +'_ParksMaps.html')
