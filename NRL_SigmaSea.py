import numpy as np
class NRL_SigmaSea_Calculeur:
    __instance = None
    def getInstance():
        if NRL_SigmaSea_Calculeur.__instance is not None:
            return NRL_SigmaSea_Calculeur.__instance
    def __init__(self,sys_info):
        NRL_SigmaSea_Calculeur.__instance = self
        #% Vilhelm Gregers-Hansen, Naval Research Laboratory
        #% 5 May 2010
        #% SigmaSea computes reflectivity coefficient for sea clutter in dB
        #% fGHz is radar frequency in GHz
        #% SS is sea state (0-7)
        #% Pol is polarization - Pol=V or Pol=H
        #% Psi is grazing angle in deg
        #% ThWind is look direction relative to wind - NOT USED by VGHSigmaSea
        #% Convert grazing angle to radians
        #% fGHz=8;
        #% SS=5;
        #% Pol='V';
        #% Psi=0:90;
        #% ThWind=0;
        self.sys_info = sys_info
        self.Psi_rad = np.deg2rad(self.sys_info.Psi)
        self.sample_data = []
        if self.sys_info.pol == 'hh':
            #% These coefficients were optimized for 0 to 60 deg grazing angle
            self.CC1= -73.0
            self.CC2= 20.781
            self.CC3= 7.351
            self.CC4= 25.65
            self.CC5= 0.0054
        elif self.sys_info.pol == 'vv':
             #% These coefficients were optimized for 0 to 60 deg grazing angle
             self.CC1= -50.796
             self.CC2= 25.93
             self.CC3= 0.7093
             self.CC4= 21.588
             self.CC5= 0.00211
        else:
            print('invalid polarization')
            
    def calculer(self, seaHeight):
        self.seaHeight = seaHeight
        import time
        start = time.time()
        self.determinerSS()
        if type(self.sys_info.Psi).__name__ == 'float':
            self.determinerPsi()
        self.preciserPsi()
        self.SigZ = self.CC1 + self.CC2*np.log10(np.sin(self.Psi_rad)) + (27.5+self.CC3*self.sys_info.Psi)*np.log10(self.sys_info.fGHz)/ (1.+0.95*self.sys_info.Psi) + self.CC4*(self.SS+1)**(1.0 /(2+0.085*self.sys_info.Psi+0.033*self.SS))+self.CC5*self.sys_info.Psi**2;
        self.sample()
        print("calculer nrl:"+str(time.time()-start))
        return self.SigZ
        #return self.getReturnRadar()
        
    def sample(self):
        self.sample_data.append(abs(self.SigZ[int(self.SigZ.shape[0]/2)][int(self.SigZ.shape[1]/2)]))
    def determinerPsi(self):
        c = 3e8
        t = 2e-7
        acc_Psi = np.zeros([len(self.seaHeight), len(self.seaHeight[0])]);
        acc_Psi[0, :] = self.sys_info.Psi
        for x in range(1, acc_Psi.shape[0]):
            acc_Psi[x, :] = self.sys_info.Psi+np.arccos((c*t)/(2*(int(x/10)+1)*30))
        self.sys_info.Psi = acc_Psi
        self.Psi_rad = np.deg2rad(self.sys_info.Psi)
    def preciserPsi(self):
        x, y = int(self.seaHeight.shape[0]/2), int(self.seaHeight.shape[1]/2)
        x_k, y_k = x+1, y+1
        z, z_x, z_y = self.seaHeight[x][y], self.seaHeight[x_k][y], self.seaHeight[x][y_k]
        k_x, k_y = z_x-z, z_y-z
        #print("k_x {} k_y {}".format(k_x, k_y))
#        fn_x = -1
#        fn_y = -k_y/k_x
#        fn_z = 1/k_x
        #切面法向量(-1,-k_y/k_x,1/k_x)
        #入射角向量(1,0,-√3)
        #夹角arccos( (a*b)/(|a|*|b|) )
        rad_Psi = np.arccos((-1-np.sqrt(3)/k_x)/(np.sqrt((k_x**2+k_y**2+1)/(k_x**2))*2))
        if rad_Psi>np.pi/2:
            rad_Psi = rad_Psi-np.pi/2
        Psi = np.rad2deg(rad_Psi)
        self.sys_info.Psi[x][y] = Psi
        self.Psi_rad[x][y] = rad_Psi    
        #print("after preciser: "+str(rad_Psi))   
    def determinerSS(self):
        self.SS = np.zeros([len(self.seaHeight), len(self.seaHeight[0])]);
        for i in range(len(self.seaHeight)):
            for j in range(len(self.seaHeight[0])):
                if 0<self.seaHeight[i][j]<1:
                    self.SS[i][j] = 1
                elif 1<self.seaHeight[i][j]<3:
                    self.SS[i][j] = 2
                elif 3<self.seaHeight[i][j]<5:
                    self.SS[i][j] = 3
                elif 5<self.seaHeight[i][j]<8:
                    self.SS[i][j] = 4
                elif 8<self.seaHeight[i][j]<12:
                    self.SS[i][j] = 5
                elif 12<self.seaHeight[i][j]<20:
                    self.SS[i][j] = 6
                elif 20<self.seaHeight[i][j]<40:
                    self.SS[i][j] = 7
        
    def getReturnRadar(self):
        # %radar  function
        # function [snr] = radar_eq(pt,freq,g,sigma,te,b,nf,loss,range)
        # %This is a program of radar eq

        pt = 1.5e+6; # % peak power in Watts
        freq = 5.6e+9; # radar operating frequency in Hz
        g = 45.0; # antenna gain in dB
        # % Pol = 'H';
        # % alpha=0.1;
        # % SS=6;
        # % Psi=0;
        # % ThWind=0;
        te = 1
        b = 1
        nf = 1
        loss = 1
        range_ = np.linspace(25e3,165e3,1000); 
        # % sigma=0.1;
        c=3.0e+8; 
        lambda_ =c/freq; 
        p_peak=10*np.log10(pt);  # convert peak power to dB
        lambda_sqdb=10*np.log10(lambda_**2);  #computr wavelength square in dB
        sigmadb=10*np.log10(np.abs(self.SigZ)); #convert sigma to dB
        four_pi_cub=10*np.log10((4*np.pi)**3);  #(4pi)^3 in dB
        k_db=10*np.log10(1.3e-23); #boltzman's constant in dB
        te_db=10*np.log10(te);  #noisetemp. in dB
        b_db=10*np.log10(b);  #bandwidth in dB
        range_pwr4_db=10*np.log10(range_**4); #vector of target range_**4 in dB
        #implement Equation(1.56)
        num=p_peak+g+g+lambda_sqdb+sigmadb; #分子
        num1=pt*g*g*lambda_*lambda_*self.SigZ
        den=four_pi_cub+k_db+te_db+b_db+nf+loss+range_pwr4_db;#分母
        den1=(4*np.pi)**3*(range_**4)*loss
        #snr=num-den;
        pr=num1/(den1)
        snr=pr
        return snr