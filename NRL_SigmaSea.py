import numpy as np
class NRL_SigmaSea_Calculeur:
    def __init__(self, fGHz = 8,Pol = 'V',Psi = 30,ThWind = 0):
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
        self.fGHz = fGHz
        self.Pol = Pol
        self.Psi = Psi
        self.ThWind = ThWind
        self.Psi_rad = np.deg2rad(self.Psi)
        self.sample_data = []
    def calculer(self, seaHeight):
        self.seaHeight = seaHeight
        self.determinerSS()
        if type(self.Psi) == int:
            self.determinerPsi()
        if self.Pol == 'H':
            #% These coefficients were optimized for 0 to 60 deg grazing angle
            self.CC1= -73.0
            self.CC2= 20.781
            self.CC3= 7.351
            self.CC4= 25.65
            self.CC5= 0.0054
        elif self.Pol == 'V':
             #% These coefficients were optimized for 0 to 60 deg grazing angle
             self.CC1= -50.796
             self.CC2= 25.93
             self.CC3= 0.7093
             self.CC4= 21.588
             self.CC5= 0.00211
        else:
            print('invalid polarization')
        self.SigZ = self.CC1 + self.CC2*np.log10(np.sin(self.Psi_rad)) + (27.5+self.CC3*self.Psi)*np.log10(self.fGHz)/ (1.+0.95*self.Psi) + self.CC4*(self.SS+1)**(1.0 /(2+0.085*self.Psi+0.033*self.SS))+self.CC5*self.Psi**2;
        self.sample()
        return self.SigZ
    def sample(self):
        self.sample_data.append(self.SigZ[int(self.SigZ.shape[0]/2)][int(self.SigZ.shape[1]/2)])
        if len(self.sample_data) > 250:
            self.sample_data = self.sample_data[1:]
    def determinerPsi(self):
        c = 3e8
        t = 2e-7
        acc_Psi = np.zeros([len(self.seaHeight), len(self.seaHeight[0])]);
        acc_Psi[0, :] = self.Psi
        for x in range(1, acc_Psi.shape[0]):
            acc_Psi[x, :] = self.Psi+np.arccos((c*t)/(2*(int(x/10)+1)*30))
        self.Psi = acc_Psi
        self.Psi_rad = np.deg2rad(self.Psi)
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
        
