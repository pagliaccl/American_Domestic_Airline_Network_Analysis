import pandas as pd
import numpy as np
from tqdm import tqdm


def generateAPSet(degreeData):
    ori=degreeData["ORIGIN"]
    dest=degreeData["DEST"]
    return np.unique(np.append(np.array(ori),np.array(dest)))


def generateDegreeMap(x):
    ret = {}
    for i in x["AIRPORT"]:
        ret[i]=0
    return ret


def mask(df, f):
    return df[f(df)]


#This is a helper function loading airport degree information
def loadDegreeData():
    degreeData =pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/finalProject/782150568_T_T100D_MARKET_US_CARRIER_ONLY.csv")[["ORIGIN","DEST"]]
    locationData =(pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/finalProject/data2.csv")[["AIRPORT","LAT_DEGREES","LON_DEGREES"]]
        .groupby(["AIRPORT"],as_index=False)
        .agg({"LAT_DEGREES": np.mean, "LON_DEGREES": np.mean})
    )
    
    apSet = generateAPSet(degreeData)
    locationData = locationData[locationData["AIRPORT"].isin(apSet)].dropna().reset_index()
    

    demap = generateDegreeMap(locationData)#setting degree hashtable
    degreeData = degreeData[degreeData["ORIGIN"].isin(demap)].dropna().reset_index()
    degreeData = degreeData[degreeData["DEST"].isin(demap)].dropna().reset_index()
    
    
    return (degreeData[['ORIGIN','DEST']],demap)


#Increment degree information along reading the data.
def addMap(x,map):
    a = x["ORIGIN"]
    b = x["DEST"]
    if a in map:
        map[a] += 1
    

#helper funciton regurn degree regarding each airport
def getDegree(x, demap):
    try:
        return demap.get(x["ORIGIN"])+demap.get(x["DEST"])
        
    except Exception as e:
        print e
        

def addResponse(x,ones):
    a = x["ORIGIN"]
    b = x["DEST"]
    if(a,b) in ones:
        return 1
    elif (b,a) in ones:
        return 1
    else:
        return 0


def helper2(x,demap):
    return demap.get(x)


def helper3(x, ret):
    ret[x['AIRPORT']] = x["AIRPORT_STATE_NAME"]


def generateStateMap():
    indata=pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/finalProject/data2.csv")[["AIRPORT", "AIRPORT_STATE_NAME"]]
    ret={}
    indata.apply(lambda x : helper3(x, ret), axis=1)
    return ret


if __name__ == '__main__':
    disMap=pd.read_csv("/Users/Pagliacci/Desktop/dick.csv")
    disMap["ORIGIN"]=disMap["AP"].str.replace('\'','').str.replace('(','').str.replace(')','').str.split(',').str[0].str.strip()
    disMap["DEST"]=disMap["AP"].str.replace('\'','').str.replace('(','').str.replace(')','').str.split(',').str[1].str.strip()

    disMap.drop("AP",1,inplace=True)

    (degreeData,demap)=loadDegreeData()

    degreeData.drop_duplicates().apply(lambda x: addMap(x,demap), axis=1)
    disMap['DEGSUM']=disMap.apply(lambda x: getDegree(x,demap),axis=1)
    disMap['ORIDEG']=disMap.apply(lambda x: helper2(x['ORIGIN'],demap),axis=1)
    disMap['DESTDEG']=disMap.apply(lambda x: helper2(x['DEST'],demap),axis=1)


    stateMap=generateStateMap()
    disMap['SAMESTATE']=disMap.apply(lambda x: 1 if stateMap.get(x['ORIGIN'])==stateMap.get(x['DEST']) else 0,axis=1)
    ones=set(tuple(x) for x in degreeData[["ORIGIN","DEST"]].to_records(index=False))
    disMap['RESPONSE'] = disMap.apply(lambda x: addResponse(x,ones),axis=1)
    
    #print final accuracy
    print disMap.head()
    print disMap["RESPONSE"].mean()
    
    #save final result
    disMap.to_csv("/Users/Pagliacci/Desktop/dick2.csv")