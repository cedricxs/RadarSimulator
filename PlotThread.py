import numpy as np
import threading
import time
from doppler import Doppler
from NRL_SigmaSea import NRL_SigmaSea_Calculeur

class plotThread (threading.Thread):   #继承父类threading.Thread
    def lognpdf(x,mu,sigma):
        return np.exp(-0.5 * ((np.log(x) - mu)/sigma)**2) / (x * np.sqrt(2*np.pi) * sigma)
        
    def __init__(self, parent):
        super().__init__()
        self.count = 0
        self.parent = parent
        self.ytheorie = None
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        while self.parent.run == True:
            start = time.time()
            self.count = self.count+1
            self.parent.sys_info.timestamp.add(1)
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
            print("plot:"+str(time.time()-start))
            time.sleep(1)
            
            
class plotDopplerThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.parent.doppler.calcul(0)
        [self.x, self.y, self.doppler] = Doppler.getInstance().getData()
        self.x_result = np.transpose(self.y[:, :100])
        self.y_result = np.transpose(self.x[:, :100])
        self.z_result = np.zeros([self.x_result.shape[0], self.x_result.shape[1]])
        self.parent.dopplerRes_widget.setDopperResultXY(self.x_result, self.y_result)
    def run(self):  
         #while self.parent.run == True:
            for i in range(self.y.shape[1]):
                start = time.time()
                self.doppler[:, i] = [v if v>10 else 0 for v in self.doppler[:, i]]
                self.parent.doppler_plot_widget.draw_doppler(self.y[:, i], self.doppler[:, i])
                self.z_result = self.z_result[1:, :]
                self.z_result  = np.append(self.z_result, [self.doppler[:, i]], axis=0)
                self.parent.dopplerRes_widget.draw_dopplerResult(self.z_result)
                print("doppler:"+str(time.time()-start))
                time.sleep(0.1)
