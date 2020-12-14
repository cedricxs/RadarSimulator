import numpy as np
import threading
import time
from doppler import Doppler
from NRL_SigmaSea import NRL_SigmaSea_Calculeur
from SeaDataGenerator import SeaData

class plotStatisticThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, parent):
        super().__init__()
        self.count = 0
        self.parent = parent
        self.ytheorie = None
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        while self.parent.plotRun == True:
            start = time.time()
            self.parent.sys_info.timestamp.add(1)
            self.count = self.count+1
            xdata = np.array(NRL_SigmaSea_Calculeur.getInstance().sample_data)
            if len(xdata)>0:
                if len(xdata)>100:
                    #最多显示100个点
                    show_data = xdata[len(xdata)-100:]
                    time_seq = range(len(xdata)-100, len(xdata))
                else:
                    show_data = xdata
                    time_seq = range(len(xdata))
                self.parent.plot_widget1.updateData([time_seq, show_data])
                if self.count%5 == 0:
                    maxdat, mindat = max(xdata), min(xdata)
                    if maxdat != mindat:
                        xaixs = np.arange(mindat, maxdat+(maxdat-mindat)/30, (maxdat-mindat)/30)
                        xpdf = np.histogram(xdata, xaixs, density=True)[0]
                        xpdf = np.append(xpdf, [0])
                        
                        if self.count%15 == 0:
                            [model, minErr, self.parent.best_Y_Theorie] = self.parent.modelFitter.fit(xaixs, xpdf)
                            if self.parent.best_Y_Theorie is not None:    
                                self.parent.plot_widget2.updateData([xaixs, xpdf, self.parent.best_Y_Theorie, [model, minErr]])
                            else: 
                                self.parent.plot_widget2.updateData([xaixs, xpdf])
            print("plot statistic:"+str(time.time()-start))
            time.sleep(1)
        
#更新三维数据并通知相关widget更新
class plotMayaviThread(threading.Thread):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
    def run(self):                   
        while self.parent.plotRun == True:
            x, y , z = SeaData.getInstance().getSeaData()
            nrl = NRL_SigmaSea_Calculeur.getInstance().getNrlData(z)
            self.parent.sys_info.z.set(z)
            self.parent.sys_info.nrl.set(nrl)
            #time.sleep(0.05)
            
class plotDopplerThread (threading.Thread):   #继承父类threading.Thread
    # 暂存暂停计数
    pos = 0
    z_result = None
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.doppler.calcul(0)
        [self.x, self.y, plotDopplerThread.doppler] = Doppler.getInstance().getData()
        self.x_result = np.transpose(self.y[:, :100])
        self.y_result = np.transpose(self.x[:, :100])
        if plotDopplerThread.z_result is None:
            plotDopplerThread.z_result = np.zeros([self.x_result.shape[0], self.x_result.shape[1]])
        self.parent.dopplerRes_widget.setDopperResultXY(self.x_result, self.y_result)
    def run(self):  
         #while self.parent.plotRun == True:
            for i in range(plotDopplerThread.pos,self.y.shape[1]):
                if self.parent.plotRun == True:
                    plotDopplerThread.pos = i
                    start = time.time()
                    plotDopplerThread.doppler[:, i] = [v if v>10 else 0 for v in plotDopplerThread.doppler[:, i]]
                    self.parent.doppler_plot_widget.draw_doppler(self.y[:, i], plotDopplerThread.doppler[:, i])
                    plotDopplerThread.z_result = plotDopplerThread.z_result[1:, :]
                    plotDopplerThread.z_result  = np.append(plotDopplerThread.z_result, [plotDopplerThread.doppler[:, i]], axis=0)
                    self.parent.dopplerRes_widget.draw_dopplerResult(plotDopplerThread.z_result)
                    print("doppler:"+str(time.time()-start))
                    time.sleep(0.1)
                else:
                    break
