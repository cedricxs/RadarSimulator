from Observer import TimeObservable, SeaDataObservable
from SeaDataGenerator import SeaData
from NRL_SigmaSea import NRL_SigmaSea_Calculeur
class System_Infomations():
    def __init__(self):
        #logdistribution
        self.sigmav = 1.0
        self.muc = 1.5
        self.sigmac = 0.6
        #doppler/logreturn
        self.xpix=250 
        self.ypix=80 
        self.nargout=0.2 
        self.pol = 'vv' 
        self.mode = 'auto'  
        #NRL
        self.fGHz = 8.0
        self.Psi = 30.0
        self.Psi_raw = 30.0
        self.ThWind = 0
        #seadata
        self.fengji = 8
        self.fengji_changed = True
        #platform 
        self.timestamp = TimeObservable()
        self.jing = 10
        self.wei = 20
        self.height = 1000
        self.x = None
        self.y = None
        self.z = SeaDataObservable()
        self.nrl = SeaDataObservable()
    def initialize(self):
        self.timestamp.set(0)
        x, y, z = SeaData.getInstance().getSeaData()
        nrl = NRL_SigmaSea_Calculeur.getInstance().getNrlData(z)
        print('for sys')
        self.x = x
        self.y = y
        self.z.set(z)
        self.nrl.set(nrl)
    def paralist(self):
        return ["载波频率","入射角","风向", "风级", "时间", "经度", "纬度", "高度"]
    def valuelist(self):
        return [self.fGHz, self.Psi_raw, self.ThWind, self.fengji, self.timestamp.value, self.jing, self.wei, self.height]
       
