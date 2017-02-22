import pandas as pd
def temp3(x, ret):
    ret[x['AIRPORT']] = x["AIRPORT_STATE_NAME"]

def generateStateMap():
    indata=pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/finalProject/data2.csv")[["AIRPORT", "AIRPORT_STATE_NAME"]]
    ret={}
    indata.apply(lambda x : temp3(x, ret), axis=1)
    return ret

if __name__ == '__main__':
    print str(i['AIRPORT']) + ':' + '[' + str(i['LONGITUDE']) + ',' + str(i['LATITUDE']) + ']' + ','