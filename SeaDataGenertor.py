import numpy as np
class SeaData:
    def __init__(self):
            self.count = 0
            self.fengji = 8
    def getSeaData(self):
        #if self.count == 0:
            dx, dy = 3, 3
            x=range(0, 300+dx, dx);
            y=range(0, 300+dy, dy);
            x, y = np.mgrid[x,y]
            self.count = self.count+1
            x, y, self.z = self.fuc(x, y)
            return [x, y, self.z]
            
#        else:
#            dx, dy = 1, 1
#            print(len(self.z), len(self.z[0]))
#            for i in range(0, len(self.z)-1):
#                self.z[i] = self.z[i+1]
#            y=range(0, 300+dy, dy);
#            x, y = np.mgrid[300:301,y]
#            x, y, update = self.fuc(x, y)
#            self.z[len(self.z)-1] = update[0]
#            self.count = self.count+1
#            return self.z
    
    #return [np.transpose(x), np.transpose(y), np.transpose(z) ]
    def fuc(self, x, y):
        fengji = self.fengji
        pinpushu=4;
        jiaodushu=30;
        h=2.8;

        wavewmin = np.array([2.438306, 1.462983, 1.044989, 0.812770, 0.664988, 0.562683, 0.487659, 0.430288]);
        wavewmax = np.array([16.444115, 9.866469, 7.047480, 5.481373, 4.484760, 3.794799, 3.288826, 2.90190]);
        wavewp = np.array([4.053570, 2.432142, 1.737244, 1.351190, 1.105519, 0.935439, 0.810714, 0.715336]);
        u=np.array([3,5,7,9,11,13,15,17])
        if fengji>8:
            fengji=8
        if fengji<1:
            fengji=1
        fi=fengji
        wmin=wavewmin[fi-1]
        wmax=wavewmax[fi-1]
        wp=wavewp[fi-1]
        ui=u[fi-1];
        M=pinpushu;
        N=jiaodushu;
        wavewn=(wmax-wmin)/M;
        thetawn=np.pi/N;
        z=np.zeros([len(x), len(x[0])]);
        for wi in range(1, M+1):  #Longuel-Higgins海浪模型
            for ki in range(1, N+1):
                theta=np.abs(-np.pi/2+(ki-1)*thetawn);#改，加了绝对值
                epsin=2*np.pi*np.random.rand();
                w=wmin+(wi-1)*wavewn+wavewn/2;
                #swi=0.81*exp(-7400/(w*ui+eps).^4)*2*(cos(theta)).^2/(pi*(w.^5+eps));%原函数
                #swi=0.81*exp(-7400/(w*ui+eps).^4)/(w.^5+eps);%pm谱，风速u的函数
                ss=0.78/(w*5)*np.exp(-3.12/(h**2)/(w**4));#ITTC谱，h为三一波高
                #an=sqrt(2*swi*wavewn*theta);
                an=np.sqrt(2*ss*wavewn*theta);
                z1=w*w*x*np.cos(theta)/9.8+w*w*y*np.sin(theta)/9.8+epsin;
                z=an*np.cos(z1)+z;

        #z = np.sin(2*x*np.pi/100)*10+np.cos(3*y*np.pi/100)*10
        return [x, y, z ]
