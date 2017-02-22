import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


if __name__ == '__main__':
    d1 = pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/RDGF1.csv")
    d2 = pd.read_csv("/Users/Pagliacci/Desktop/PHY 525/phy525TemporaryData/RDGF2.csv")
    allD = pd.DataFrame({'configuration_model': d2['value'], 'p_soft_decision': d1['value'], 'p_hard_decision': 0.494989794025})

    plt.figure(1)
    axes=allD[['p_soft_decision', 'p_hard_decision']].plot()
    print np.mean(d1['value'])
    print np.std(d1['value'])

    #plot1
    plt.axhline(np.mean(d1['value']), color='r')

    plt.plot(np.mean(d2['value'])*100,color='blue')
    plt.plot(np.mean(d1['value'])*100,color='red')
    plt.show()

    #plot2
    plt.close()
    bar=pd.DataFrame({'configuration_model': np.mean(d2['value']),'p_soft_decision': np.mean(d1['value']),'p_hard_decision': 0.494989794025},index=[1])
    plt.figure(2)
    bar.ix[1].plot(kind='bar',color=['r','b','g'],stacked=True)
    plt.show()




