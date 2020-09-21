import numpy as np
class SeaData:
    def __init__(self, sys_info):
        self.sys_info = sys_info
        self.fengji = sys_info.fengji
        self.pinpushu=4;
        self.jiaodushu=30;
        self.h=2.8;

        self.wavewmin = np.array([2.438306, 1.462983, 1.044989, 0.812770, 0.664988, 0.562683, 0.487659, 0.430288]);
        self.wavewmax = np.array([16.444115, 9.866469, 7.047480, 5.481373, 4.484760, 3.794799, 3.288826, 2.90190]);
        self.wavewp = np.array([4.053570, 2.432142, 1.737244, 1.351190, 1.105519, 0.935439, 0.810714, 0.715336]);
        self.u=np.array([3,5,7,9,11,13,15,17])
        if self.fengji>8:
            self.fengji=8
        if self.fengji<1:
            self.fengji=1
        dx, dy = 3, 3
        x = range(0, 300, dx);
        y = range(0, 300, dy);
        self.x, self.y = np.mgrid[x,y]
        self.z_zeros = np.zeros([len(self.x), len(self.x[0])]);
        self.fi=self.fengji
        self.wmin=self.wavewmin[self.fi-1]
        self.wmax=self.wavewmax[self.fi-1]
        self.wp=self.wavewp[self.fi-1]
        self.ui=self.u[self.fi-1];
        self.M=self.pinpushu;
        self.N=self.jiaodushu;
        self.wavewn=(self.wmax-self.wmin)/self.M;
        self.thetawn=np.pi/self.N;
        self.theta=[np.abs(-np.pi/2+ki*self.thetawn) for ki in range(self.N)]#改，加了绝对值
        self.ctheta9 = np.cos(self.theta)/9.8
        self.stheta9 = np.sin(self.theta)/9.8
        self.w=[self.wmin+wi*self.wavewn+self.wavewn/2 for wi in range(self.M)];
        self.w2x = [(w**2)*self.x for w in self.w]
        self.w2y = [(w**2)*self.y for w in self.w]
        self.ss=[0.78/(w*5)*np.exp(-3.12/(self.h**2)/(w**4)) for w in self.w]#ITTC谱，h为三一波高
        self.an=[np.sqrt(2*ss*self.wavewn*theta) for ss in self.ss for theta in self.theta]
        self.w2xctheta9 = [w2x*ctheta9 for w2x in self.w2x for ctheta9 in self.ctheta9]
        self.w2ystheta9 = [w2y*stheta9 for w2y in self.w2y for stheta9 in self.stheta9]
        self.w2xy = [w2xctheta9+w2ystheta9 for (w2xctheta9, w2ystheta9) in zip(self.w2xctheta9, self.w2ystheta9)]
    def update_para(self):
        self.fengji = self.sys_info.fengji
        if self.fengji>8:
            self.fengji=8
        if self.fengji<1:
            self.fengji=1
        self.z_zeros = np.zeros([len(self.x), len(self.x[0])]);
        self.fi=self.fengji
        self.wmin=self.wavewmin[self.fi-1]
        self.wmax=self.wavewmax[self.fi-1]
        self.wp=self.wavewp[self.fi-1]
        self.ui=self.u[self.fi-1];
        self.M=self.pinpushu;
        self.N=self.jiaodushu;
        self.wavewn=(self.wmax-self.wmin)/self.M;
        self.thetawn=np.pi/self.N;
        self.theta=[np.abs(-np.pi/2+ki*self.thetawn) for ki in range(self.N)]#改，加了绝对值
        self.ctheta9 = np.cos(self.theta)/9.8
        self.stheta9 = np.sin(self.theta)/9.8
        self.w=[self.wmin+wi*self.wavewn+self.wavewn/2 for wi in range(self.M)];
        self.w2x = [(w**2)*self.x for w in self.w]
        self.w2y = [(w**2)*self.y for w in self.w]
        self.ss=[0.78/(w*5)*np.exp(-3.12/(self.h**2)/(w**4)) for w in self.w]#ITTC谱，h为三一波高
        self.an=[np.sqrt(2*ss*self.wavewn*theta) for ss in self.ss for theta in self.theta]
        self.w2xctheta9 = [w2x*ctheta9 for w2x in self.w2x for ctheta9 in self.ctheta9]
        self.w2ystheta9 = [w2y*stheta9 for w2y in self.w2y for stheta9 in self.stheta9]
        self.w2xy = [w2xctheta9+w2ystheta9 for (w2xctheta9, w2ystheta9) in zip(self.w2xctheta9, self.w2ystheta9)]
    def getSeaData(self):
        import time 
        start = time.time()
        self.z = self.fuc()
        print("generetor sea data:"+str(time.time()-start))
        return [self.x, self.y, self.z]
            
    def fuc(self):
        z=self.z_zeros.copy()
        for wi in range(self.M):  #Longuel-Higgins海浪模型
            for ki in range(self.N):
                epsin=2*np.pi*np.random.rand()
                index = self.N*wi+ki
                an=self.an[index]
                z1=self.w2xy[index]+epsin
                z=an*np.cos(z1)+z
        #z = np.sin(2*x*np.pi/100)*10+np.cos(3*y*np.pi/100)*10
        return z
