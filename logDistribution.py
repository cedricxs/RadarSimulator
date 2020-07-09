#function xdata = py_logdistribution(azi_num)
import numpy as np
from spectrum.burg import pburg
import matplotlib.pyplot as plt
class LogDistribution:
    def __init__(self):
        self.setSigmav(1.0)
        self.setMuc(1.5)
        self.setSigmac(0.6)

        
    def setSigmav(self, sigmav):
        self.sigmav = sigmav
        
    def setMuc(self, muc):
        self.muc = muc
        
    def setSigmac(self, sigmac):
        self.sigmac = sigmac
        
    def gererTimeDomineData(self, nb_point):
        self.fr = 1000
        
        lamda0 = 0.05
        self.sigmaf = 2*self.sigmav/lamda0
        
        d1 = np.random.rand(nb_point)
        d2 = np.random.rand(nb_point)
        
        xi=1*np.multiply(np.sqrt(-2*np.log(d1)), np.cos(2*np.pi*d2))
        #xq=2*np.multiply(np.sqrt(-2*np.log(d1)), np.sin(2*np.pi*d2))
        
#    %azi_num=2000;%图1横轴数据点
#    fr=1000;
#
#    lamda0=0.05;
#    sigmav=1.0;
#    sigmaf=2*sigmav/lamda0;
#
#    rand('state',sum(100*clock));
#    d1=rand(1,azi_num);
#    rand('state',7*sum(100*clock)+3);
#    d2=rand(1,azi_num);
#    xi=1*(sqrt(-2*log(d1)).*cos(2*pi*d2));
#    xq=2*sqrt(-2*log(d1)).*sin(2*pi*d2);
#
        coeff = []
        coe_num = 12
        for n in range(coe_num+1):
            coeff.append(2*self.sigmaf*np.sqrt(np.pi)*np.exp(-4*(self.sigmaf*np.pi*n/self.fr)**2)/self.fr)
    

#    coe_num=12;
#    for n=0:coe_num
#        coeff(n+1)=2*sigmaf*sqrt(pi)*exp(-4*sigmaf^2*pi^2*n^2/fr^2)/fr;
#    end

        b =[]
        for n in range(1, 2*coe_num+2, 1):
            if n <= coe_num+1:
                b.append(1/2*coeff[coe_num+2-n-1])
            else:
                b.append(1/2*coeff[n-coe_num-1])
#    for n=1:2*coe_num+1
#        if n<=coe_num+1
#            b(n)=1/2*coeff(coe_num+2-n);
#        else
#            b(n)=1/2*coeff(n-coe_num);
#        end
#    end
#    %Gaussion clutter generation
        xxi = np.convolve(b, xi)
        xxi = xxi[coe_num*2:nb_point+coe_num*2]
#    xxi=conv(b,xi);
#    xxi=xxi(coe_num*2+1:azi_num+coe_num*2);
        xisigmac = np.std(xxi)
        ximuc = np.mean(xxi)
        yyi = (xxi-ximuc)/xisigmac

#    xisigmac=std(xxi);
#    ximuc=mean(xxi);
#    yyi=(xxi-ximuc)/xisigmac;

        yyi = self.sigmac*yyi+np.log(self.muc)
        self.xdata = np.exp(yyi)
#        return self.xdata.tolist()
#    muc=1.5;
#    sigmac=0.6;
#    yyi=sigmac*yyi+log(muc);
#    xdata=exp(yyi);

    def gereProbaDistribution(self):
        num=100;
        maxdat=max(abs(self.xdata));
        mindat=min(abs(self.xdata));
        NN, bin=np.histogram(abs(self.xdata),num);
        self.xpdf1=num*NN/(sum(NN)*(maxdat-mindat));
        self.xaxis1= np.arange(mindat, maxdat-(maxdat-mindat)/num+(maxdat-mindat)/num-0.001, (maxdat-mindat)/num)
        self.th_val = self.lognpdf(self.xaxis1,np.log(self.muc),self.sigmac);
#        figure;plot(xaxis1,xpdf1);
#        hold,plot(xaxis1,th_val,':r');
#        return [xaxis1, xpdf1, th_val]
        
        
    def lognpdf(self, x, mu, sigma):
        return np.exp(-0.5 * ((np.log(x) - mu)/sigma)**2) / (x * np.sqrt(2*np.pi) * sigma); 
        
    def updateData(self):
        self.gererTimeDomineData(2000)
        self.gereProbaDistribution()
        self.gerepuissance()
    def gerepuissance(self):
        sg=self.xdata;
        sg=sg-np.mean(sg);

        M=128;
        pobjet=pburg(np.real(sg),16,NFFT=M,sampling=self.fr);
        pobjet()
        self.psd_dat = pobjet.psd
        self.psd_dat=self.psd_dat/(max(self.psd_dat));
        self.freqx= np.arange(0, int(0.5*M)+1, 1)
        self.freqx=self.freqx*self.fr/M;
        self.powerf=np.exp(-self.freqx**2/(2*self.sigmaf**2));
        #plt.plot(self.freqx,self.psd_dat);
        #plt.plot(self.freqx,self.powerf,'--');
        #plt.show()

if __name__ == '__main__':
    log = LogDistribution()
    log.updateData()
    log.puissance()
    
