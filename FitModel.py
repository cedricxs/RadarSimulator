from scipy.optimize import curve_fit
from scipy.special import kv, gamma

import numpy as np
from enum import IntEnum
class ModelFitter:

    def __init__(self):
        pass
    def MAE(self, y, yfit):
        return ((np.abs((y-yfit))).sum())/len(y)
    def bestFitter(self, MAEs):
        min, index = MAEs[0], 0
        for i in range(1, len(MAEs)):
            if MAEs[i] < min:
                index = i
                min = MAEs[i]
        return [min, index+1]
    def fit(self, x, y):
        try:
            popt1, pcov1 = curve_fit(DistributionModel.lognpdfModel,  x, y)#训练函数
            popt2, pcov2 = curve_fit(DistributionModel.kDistribution,  x, y, bounds=([0, 0], [100, 100]))#训练函数
            popt3, pcov3 = curve_fit(DistributionModel.rayliDistribution,  x, y, bounds=([0], [100]))#训练函数
            popt4, pcov4 = curve_fit(DistributionModel.weibullDistribution,  x, y, bounds=([0, 0], [100, 100]))#训练函数
            #参数估计的标准差
#            perr1  = np.sqrt(np.diag(pcov1))[0]
#            perr2  = np.sqrt(np.diag(pcov2))[0]
#            perr3  = np.sqrt(np.diag(pcov3))[0]
#            perr4  = np.sqrt(np.diag(pcov4))[0]
            y_Theorie1 = DistributionModel.lognpdfModel(x, popt1[0], popt1[1])
            y_Theorie2 = DistributionModel.kDistribution(x, popt2[0], popt2[1])
            y_Theorie3 = DistributionModel.rayliDistribution(x, popt3[0])
            y_Theorie4 = DistributionModel.weibullDistribution(x, popt4[0], popt4[1])
            minErr, model = self.bestFitter([self.MAE(y, y_Theorie1), self.MAE(y, y_Theorie2), self.MAE(y, y_Theorie3), self.MAE(y, y_Theorie4)])
            if model == DistributionModel.Logn:
                y_Theorie = y_Theorie1
                print("para : {} {}".format(popt1[0], popt1[1]))
            elif model == DistributionModel.K:
                y_Theorie = y_Theorie2
            elif model == DistributionModel.Rayli:
                y_Theorie = y_Theorie3
            elif model == DistributionModel.Weibull:
                y_Theorie = y_Theorie4
            return [model, minErr, y_Theorie]
        except:
            return [0, 0, None]
    
    def fitLog(self, x, y):
        popt1, pcov1 = curve_fit(DistributionModel.lognpdfModel,  x, y, absolute_sigma = True)#训练函数
        y_Theorie = DistributionModel.lognpdfModel(x, popt1[0], popt1[1])
        perr1  = np.sqrt(np.diag(pcov1))[0]
        return [DistributionModel.Logn, perr1, y_Theorie]
        
        
        
class DistributionModel(IntEnum):
    Logn = 1
    K = 2
    Rayli = 3
    Weibull = 4
    def lognpdfModel(x,mu,sigma):
        return np.exp(-0.5 * ((np.log(x) - mu)/sigma)**2) / (x * np.sqrt(2*np.pi) * sigma)
    #kv(v, z) Modified Bessel function of the second kind of real order v
    def kDistribution(x, alpha, vmuc):
        return 2*((x/(2*alpha))**vmuc)*kv((vmuc-1),x/alpha)/(alpha*gamma(vmuc))
    def rayliDistribution(x, sigmac):
        return (x/sigmac**2)*np.exp(-x**2/(2*sigmac**2))
    def weibullDistribution(x, p, q):
        return p*(x**(p-1))*np.exp(-(x/q)**p)/(q**p)
