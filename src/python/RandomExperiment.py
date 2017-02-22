import pandas as pd
from termcolor import colored
import sklearn
import numpy as np
from sklearn.linear_model import LogisticRegression
from tqdm import tqdm


def generateMap(x,temp):
    temp[x['DEST']] = x['PROB']


def creatProbMap(train):
    # train = pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/dick2.csv", index_col=0)
    lr = LogisticRegression()
    lr.fit(X=train[['DEGSUM', 'DIST','ORIDEG','DESTDEG','SAMESTATE']], y=train['RESPONSE'])
    train["PROB"]=[j for i, j  in lr.predict_proba(X=train[['DEGSUM', 'DIST','ORIDEG','DESTDEG','SAMESTATE']])]

    # print sklearn.metrics.classification_report(y_true=train['RESPONSE'],y_pred=lr.predict(X=train[['DEGSUM', 'DIST','ORIDEG','DESTDEG','SAMESTATE']]))
    grouped=train.sort('ORIDEG').groupby('ORIGIN')
    ret={}
    for name, group in tqdm(grouped):
        temp={}
        group.dropna().reset_index().apply(lambda x: generateMap(x,temp), axis=1)
        ret[name]=temp
    print colored("\n MAP CREATED \n",'green')
    return (ret,grouped)


def normalizeTo1(inList):
    denominator=sum(inList)
    return [i/denominator for i in inList]


def generateOneRandomGraph(data, dict):
    ret=[]
    for name,group in data:
        if name=='':
            continue
        possibleDest=dict[name]
        result=np.random.choice(possibleDest.keys(),p=normalizeTo1(possibleDest.values()),replace=False,size=group['ORIDEG'].mean())
        for i in result:
            ret.append((name, i))
    return ret


def generateOneRandomGraph2(data, dict):
    ret=[]
    for name,group in data:
        if name=='':
            continue
        possibleDest=dict[name]
        result=np.random.choice(possibleDest.keys(),replace=False,size=group['ORIDEG'].mean())
        for i in result:
            ret.append((name, i))
    return ret


def generateOneRandomGraph3():
    data = pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/dick2.csv", index_col=0)
    targeted = data[data['RESPONSE'] == 1][['ORIGIN', 'DEST']]
    targeted = [tuple(x) for x in targeted.values]

    (probMap, groupData) = creatProbMap(data)
    ret = []
    for name, group in groupData:
        if name == '':
            continue
        i=group.sort('PROB',ascending=False).reset_index()
        sampleSize=int(group['ORIDEG'].mean())
        result = i.head(sampleSize)['DEST']
        for j in result:
            ret.append((name, j))
    return compareTwoGraph(ret,targeted)


def compareTwoGraph(generated,targeted):
    return len(set(targeted) & set(generated))/float(len(set(targeted)))


def generatedMutipleGraph(n):
    data = pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/dick2.csv", index_col=0)
    (probMap, groupData) = creatProbMap(data)
    targeted = data[data['RESPONSE'] == 1][['ORIGIN', 'DEST']]
    targeted = [tuple(x) for x in targeted.values]
    ret=[]
    for i in tqdm(range(n)):
        generated=generateOneRandomGraph(groupData,probMap)
        ret.append(compareTwoGraph(generated,targeted))
    return ret


def generatedMutipleGraph2(n):
    data = pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/dick2.csv", index_col=0)
    (probMap, groupData) = creatProbMap(data)
    targeted = data[data['RESPONSE'] == 1][['ORIGIN', 'DEST']]
    targeted = [tuple(x) for x in targeted.values]
    ret=[]
    for i in tqdm(range(n)):
        generated=generateOneRandomGraph2(groupData,probMap)
        ret.append(compareTwoGraph(generated,targeted))
    return ret

def findJFK():
    data = pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/dick2.csv", index_col=0)
    (probMap, groupData) = creatProbMap(data)
    return groupData.get_group('ORD').sort('PROB',ascending=False)[['DEST','PROB']]


def outputOneGraph():
    data = pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/dick2.csv", index_col=0)
    (probMap, groupData) = creatProbMap(data)
    ret = []
    for name, group in groupData:
        if name == '':
            continue
        possibleDest = probMap[name]
        result = np.random.choice(possibleDest.keys(), replace=False, size=group['ORIDEG'].mean())
        for i in result:
            ret.append((name, i))
    return ret


if __name__ == '__main__':
    n=100
    # data = generatedMutipleGraph(n)
    # print np.mean(data)
    # RDGF1=pd.DataFrame({'value':data}).to_csv('/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/RDGF1.csv',index=False)

    # data2 = generatedMutipleGraph2(n)
    # print np.mean(data2)
    # RDGF2=pd.DataFrame({'value':data2}).to_csv('/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/RDGF2.csv',index=False)
    #
    #
    # data3 = generateOneRandomGraph3()
    # data3 = generateOneRandomGraph3()
    # print data3

    # findJFK()

    # outdata=outputOneGraph()
    # RDGF2 = pd.DataFrame({'value': outdata}).to_csv('/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/result.csv', index=False)


    # result2=findJFK()
    # result2.to_csv('/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/result3.csv', index=False)