import numpy as np
#import pandas as pd
import math
class LogReturnRadar:
    def __init__(self, sys_info):
        self.sys_info = sys_info
        import netCDF4
        self.file = r'#310_19931118_162155_stareC0000.cdf'
        #self.file = '#17_19931107_135603_starea.cdf';
        self.content = netCDF4.Dataset(self.file)
        #print(content)
        #print(content.variables['adc_data'].shape)#显示nc文件的所有结构，以便大概了解里面的内容
        self.data = self.content.variables['adc_data']
        #print('data:', self.data[0, 0, 0, 0])
        #print(self.content.variables['adc_data'])
        self.azi = np.array(self.content.variables['azimuth_angle'])
        #azi = pd.DataFrame(self.azi);
        #print(azi.describe(include='all'))
        #pd.options.display.max_columns = None
        #pd.options.display.max_rows = None
        #np.set_printoptions(threshold=np.inf)
        #print(azi.iloc[:, -1].value_counts());
        #print(self.content.variables['elevation_angle'])
        self.shapes = self.data.shape
        self.nsweep=self.shapes[0]
        self.nrange = self.shapes[2]
        self.xavg = max(1,math.ceil(self.nsweep/self.sys_info.xpix));#ceil朝正无穷大方向取整，max(a,b),如果b小于a，则等于a

        self.scan_range=self.content.variables['range']

        #% txpol = 'vv'; % hh, hv, vh, vv
        self.data = np.transpose(self.data, (0, 1, 2, 3))
        self.data = self.data.astype('short') 
        #           % 'auto' (automatic pre-processing) 
        #           % '' (pre-processing for dartmouth files containing land)
        #
        #%% If try to use the data of 93, use this part to correct the data %%          
        #    
        v = self.data<0
        self.data[v] = self.data[v]+256
    
    def calcul(self):
        # 雷达返回
        A=np.zeros([self.nrange,math.floor(self.nsweep/self.xavg)])

        lenAmpl=self.xavg*math.floor(self.nsweep/self.xavg)
      
        for rangebin in range(self.nrange):
            from ipixLoader import ipixLoader 
            [I,Q,meanIQ,stdIQ,inbal] = ipixLoader(self.data,self.sys_info.pol,rangebin,self.sys_info.mode)
            absiq=abs(I+1j*Q)*math.sqrt(stdIQ[0]*stdIQ[1])
        #% prod元素的乘积
            ampl=absiq[0:lenAmpl];#绝对值
            ampl = ampl.reshape(self.xavg,math.floor(self.nsweep/self.xavg), order='F')
            A[rangebin,:]=np.mean(ampl,0)
        #end
        #
        #% PRF=nc{'PRF'}(1);
        PRF=self.content.variables['PRF']
        PRF = PRF[0]
        #% time=(1:size(A,2))/PRF*xavg;
        
        
        
        x_time=np.arange(A.shape[1])/PRF*self.xavg
        #% range=nc{'range'}(:);
        #
        #% range averaging
        while A.shape[0]>self.sys_info.ypix:
          A=0.5*(A[0:A.shape[0]-1:2,:]+A[1:A.shape[0]:2,:])
          self.scan_range=0.5*(self.scan_range[0:self.scan_range.shape[0]-1:2]+self.scan_range[1:self.scan_range.shape[0]:2]);
        #end
        #
        #% indexed color log plot
        logA=np.log(A)
        mn=np.amin(logA); mx=np.amax(logA)
        logA=(logA-mn)*63/(mx-mn)
        logA = logA.tolist()
        #
        if self.sys_info.nargout<1:
            return [x_time,self.scan_range, logA]
            
if __name__ == '__main__':    
    from matplotlib import pyplot as plt
    fig = plt.figure()
    #定义画布为1*1个划分，并在第1个位置上进行作图
    ax = fig.add_subplot(111)
    ax.set_title('time doppler')
    ax.set_xlabel('time(s)')
    ax.set_ylabel('doppler(m/s)')
    from System_Infomations import System_Infomations
    log = LogReturnRadar(System_Infomations())
    xx, yy, logTD = log.calcul()
    im = ax.pcolormesh(xx,yy,logTD, cmap='jet')
    plt.show()
