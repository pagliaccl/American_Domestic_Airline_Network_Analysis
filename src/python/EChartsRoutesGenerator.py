import pandas as pd
import numpy as np
import csv

def generateLocationMap():
    apAndProb=pd.read_csv('/Users/Pagliacci/Desktop/result3.csv').head(100)
    locationData = (
    pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/finalProject/data2.csv")[["AIRPORT", "LATITUDE", "LONGITUDE"]]
    .groupby(["AIRPORT"], as_index=False)
    .agg({"LATITUDE": np.mean, "LONGITUDE": np.mean})
    )
    join = apAndProb.merge(locationData, left_on='AIRPORT',right_on='AIRPORT')
    join['PROB']=join['PROB']*100

    with open('/Users/Pagliacci/Desktop/location2.csv', 'w') as fp:
        join.apply(lambda i: fp.writelines('\''+(i['AIRPORT']+'\''+':'+ '['+str(i['LONGITUDE'])+','+str(i['LATITUDE'])+']'+','+'\n')), axis=1)
           
def generateRoute():
    apAndProb = pd.read_csv('/Users/Pagliacci/Desktop/result3.csv').head(100)
    locationData = (
        pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/finalProject/data2.csv")[["AIRPORT", "LATITUDE", "LONGITUDE"]]
            .groupby(["AIRPORT"], as_index=False)
            .agg({"LATITUDE": np.mean, "LONGITUDE": np.mean})
    )
    join = apAndProb.merge(locationData, left_on='AIRPORT', right_on='AIRPORT')
    join['PROB'] = join['PROB'] * 100

    with open('/Users/Pagliacci/Desktop/route2.csv', 'w') as fp:
        join.apply(lambda x: fp.writelines('['+'{'+'name'+':'+'\''+'ORD'+'\''+'}'+','+'{'+'name'+':'+'\''+x['AIRPORT']+'\''+','+'value'+':'+str(x['PROB'])+'}'+']'+','+'\n'),axis=1)


if __name__ == '__main__':
    generateLocationMap()
