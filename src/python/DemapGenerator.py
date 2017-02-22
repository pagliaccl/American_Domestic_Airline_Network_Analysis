from collections import defaultdict
import numpy as np
import pandas as pd
from tqdm import tqdm
import math


def toRad(x):
    return math.pi*x/180.


def calculateDistance(lat1,lon1,lat2,lon2):
    R = 6371
    dLat=toRad(lat1-lat2)
    dLon=toRad(lon1-lon2)
    lat1=toRad(lat1)
    lat2=toRad(lat2)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.sin(dLon / 2) * math.sin(dLon / 2) * math.cos(lat1) * math.cos(lat2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


def generateDistanceMap(x,locMap):
    ret = {}

    for i in tqdm(range(len(x))):
        for j in range(len(x)):
                lat1=float(locMap[x[i]][0])
                lon1=float(locMap[x[i]][1])
                lat2=float(locMap[x[j]][0])
                lon2=float(locMap[x[j]][1])
                ret[(x[i],x[j])]=calculateDistance(lat1,lon1,lat2,lon2)
    return ret


def generateDegreeMap(x):
    ret = {}
    for i in x["AIRPORT"]:
        ret[i]=0
    return ret


def addLocMap(x,map):
    ap=x["AIRPORT"]
    a=x["LAT_DEGREES"]
    b=x["LON_DEGREES"]
    map[ap]=(a,b)


def addMap(x,map):
    a = x["ORIGIN"]
    b = x["DEST"]
    if a in map:
        map[a] += 1
    if b in map:
        map[b] += 1


def mask(df, f):
  return df[f(df)]


def generateAPSet(degreeData):
    temp1=degreeData["ORIGIN"]
    temp2=degreeData["DEST"]
    return np.unique(np.append(np.array(temp1),np.array(temp2)))


def addDegreeToLoc(x,demap):
    x['DEG']=demap.get(x['AIRPORT'])

if __name__ == '__main__':
    degreeData =pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/finalProject/782150568_T_T100D_MARKET_US_CARRIER_ONLY.csv")[["ORIGIN","DEST"]]
    locationData=(pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/finalProject/data2.csv")[["AIRPORT","LAT_DEGREES","LON_DEGREES"]]
        .groupby(["AIRPORT"],as_index=False)
        .agg({"LAT_DEGREES": np.mean, "LON_DEGREES": np.mean})
    )
    apSet = generateAPSet(degreeData)

    locationData = locationData[locationData["AIRPORT"].isin(apSet)].dropna().reset_index()

    # initialize Two Map
    demap=generateDegreeMap(locationData)
    degreeData=degreeData[degreeData["ORIGIN"].isin(demap)]
    degreeData=degreeData[degreeData["DEST"].isin(demap)].dropna().reset_index()

    locationMap={}

    # updateValue
    degreeData.apply(lambda x: addMap(x,demap), axis=1)
    locationData.apply(lambda x: addLocMap(x,locationMap),axis=1)
    locationData['DEG']=locationData['AIRPORT'].apply(lambda x: demap.get(x))


    #generating result
    disMap=generateDistanceMap(locationData["AIRPORT"],locationMap)
    print "disMap Created, Saving DataFrame"

    ret=pd.DataFrame.from_dict(disMap,orient="index")
    ret.to_csv("/Users/Pagliacci/Desktop/dick.csv")
