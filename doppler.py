import numpy as np
import math
class Doppler:
    __instance = None
    def getInstance():
        if Doppler.__instance is not None:
            return Doppler.__instance
            
    def __init__(self, sys_info):
        Doppler.__instance = self
        self.sys_info = sys_info  
        import netCDF4
        self.file = r'#310_19931118_162155_stareC0000.cdf'
        self.content = netCDF4.Dataset(self.file)
        #print(content)
        #print(content.variables['adc_data'].shape)#显示nc文件的所有结构，以便大概了解里面的内容
        self.data = self.content.variables['adc_data']
        self.shapes = self.data.shape
        self.nsweep=self.shapes[0]
        self.n = self.shapes[2]
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

    def calcul(self, rangebin):
        #% Time Doppler plot
        #
        #% load I and Q data
        #%[I,Q]=ipixcdf(nc,txpol,rangebin);
        from ipixLoader import ipixLoader 
        [I,Q,meanIQ,stdIQ,inbal] = ipixLoader(self.data,self.sys_info.pol,rangebin,self.sys_info.mode);
        #R = abs(I + 1j * Q);
        #r = R / max(R);

        N=I.shape[0];#%r=size(A,1)该语句返回的时矩阵A的行数， c=size(A,2) 该语句返回的时矩阵A的列数。
        #
        #% adjust fft window and averaging to match image size
        wdw=max(128,2**math.ceil(np.log(4*N/self.sys_info.xpix)/np.log(2)));#128
        yavg=max(1,math.ceil(wdw/self.sys_info.ypix));#1
        timeStep=wdw/4;#32
        M=math.floor((N-wdw)/timeStep);# y = floor(x) 函数将x中元素取整，值y为不大于本身的最大整数。
        #%对于复数，分别对实部和虚部取整
        #
        # short time fourier transforms
        #hw=np.hamming(wdw);#设置汉明窗，wdw为汉明窗的长度
        TD=np.zeros([math.floor(wdw/yavg),M]);#B = zeros(m,n) or B = zeros([m n])  返回一个m x n的零矩阵
         
        leny=yavg*math.floor(wdw/yavg)
        for m in range(M):
            i= int(m*timeStep)
            x=I[i:wdw+i]+1j*Q[i:wdw+i]
            #  %x=hw.*(I(1+i:wdw+i)+j*Q(1+i:wdw+i));
            fftx=abs(np.fft.fftshift(np.fft.fft(x)))
            y=fftx[:leny]
            y = y.reshape(yavg,math.floor(wdw/yavg), order='F')
            TD[:,m]=np.mean(y, 0);#mean(A,1)就是包含每一列的平均值的行向量 
        #end
        #
        #% time and normalized frequency
        #%PRF=nc{'PRF'}(1);              % Pulse Repetition Frequency [Hz]
        PRF=self.content.variables['PRF']
        PRF = PRF[0]
        x_time=np.array([0, M/PRF])
        freq=np.array([-0.5*PRF, 0.5*PRF])
        #
        #% convert to doppler velocity转换成多普勒速度
        RF_frequency=self.content.variables['RF_frequency']
        RF_frequency=RF_frequency[0]
        #%doppl=freq*3e8/(2*nc{'RF_frequency'}(1)*1e9); 
        doppl=freq*3e8/(2*RF_frequency*1e9); 
        #% enhance log-plot with noise floor
        mn=np.mean(TD,1);#mean(A,2)就是包含每一行的平均值的列向量
        [mn,indx]=np.sort(mn), np.argsort(mn)#升序排列，矩阵大小不变，indx为元素原位置
        noise=TD[indx[0:1],:]
        noiseFloor=np.median(noise[:]);#按每列返回一个值,为该列从大到小排列的中间值
        TD_small_noiseFloor = TD<noiseFloor
        TD[TD_small_noiseFloor] = noiseFloor
        logTD=np.log(TD)
        mn=np.amin(logTD)
        mx=np.amax(logTD)
        self.logTD=(logTD-mn)*63/(mx-mn)
    
    
    
        #
        #% display image
        if self.sys_info.nargout<1:
          x_time=[(wdw/2+i*timeStep)/PRF for i in range(M)];
          freq=np.array([(i/(wdw/yavg)-0.5)*PRF for i in range(math.floor(wdw/yavg))]);
          doppl=freq*3e8/(2*RF_frequency*1e9); 
          doppl = doppl.tolist()
          self.xx, self.yy = np.meshgrid(x_time,doppl)
        
        #return [self.xx, self.yy, self.logTD]
        
    def getData(self):
        return [self.xx, self.yy, self.logTD]
            
if __name__ == '__main__':    
    import os
    import PyQt5
    dirname = os.path.dirname(PyQt5.__file__)
    plugin_path = os.path.join(dirname, 'Qt','plugins', 'platforms')
    os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path
    from matplotlib import pyplot as plt
    from System_Infomations import System_Infomations
    fig = plt.figure()
    #定义画布为1*1个划分，并在第1个位置上进行作图
    ax = fig.add_subplot(111)
    ax.set_title('time doppler')
    ax.set_xlabel('time(s)')
    ax.set_ylabel('doppler(m/s)')
    doppler = Doppler(System_Infomations())
    doppler.calcul(1)
    xx, yy, logTD = doppler.getData()
    im = ax.pcolormesh(xx,yy,logTD, cmap='jet')
    plt.show()
