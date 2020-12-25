from PyQt5 import QtWidgets
from Ui_radarPage import Ui_Form
from PyQt5.QtCore import pyqtSlot, Qt
from Mayavi_Widget import MayaviQWidget
class RadarPage(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self, sys_info, parent=None):
        super(RadarPage, self).__init__(parent)
        self.setupUi(self)
        self.sys_info = sys_info 
        self.setWindowFlags(Qt.FramelessWindowHint)

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.sys_info.appStatus.set('targetPage')
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        self.plot3d_nrl_widget.close()
        self.close()

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        self.sys_info.radarColormap = 'winter'
        self.plot3d_nrl_widget.updateColormap(self.sys_info.radarColormap)

    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        self.sys_info.radarColormap = 'blue-red'
        self.plot3d_nrl_widget.updateColormap(self.sys_info.radarColormap)

    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        self.sys_info.radarColormap = 'ocean'
        self.plot3d_nrl_widget.updateColormap(self.sys_info.radarColormap)

    @pyqtSlot(int)
    def on_comboBox_activated(self, index):
        self.sys_info.fengji = index+1 
        self.sys_info.seaDataGen.update_para()
        self.plot3d_nrl_widget.updateStaticView(self.sys_info.nrlDataGen.getNrlData(self.sys_info.seaDataGen.getSeaData()[2]))
        

    def show(self):
        self.move(self.sys_info.desktopWidth*0.15, self.sys_info.desktopHeight*0.15)
        self.resize(self.sys_info.desktopWidth*0.7, self.sys_info.desktopHeight*0.7)  
        super().show()
        self.comboBox.setCurrentIndex(self.sys_info.fengji-1)

    def resizeEvent(self,event):
        self.plot3d_nrl_widget = MayaviQWidget(self.sys_info, self.widget_19, 1)