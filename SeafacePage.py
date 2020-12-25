from PyQt5 import QtWidgets
from Ui_seafacePage import Ui_Form
from PyQt5.QtCore import pyqtSlot, Qt
from Mayavi_Widget import MayaviQWidget

class SeafacePage(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self, sys_info, parent=None):
        super(SeafacePage, self).__init__(parent)
        self.setupUi(self)
        self.sys_info = sys_info
        self.setWindowFlags(Qt.FramelessWindowHint)
        

    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.sys_info.appStatus.set('radarPage')
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        self.plot3d_z_widget.close()
        self.close()

    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        self.sys_info.seafaceColormap = 'winter'
        self.plot3d_z_widget.updateColormap(self.sys_info.seafaceColormap)
    @pyqtSlot()
    def on_pushButton_6_clicked(self):
        self.sys_info.seafaceColormap = 'gray'
        self.plot3d_z_widget.updateColormap(self.sys_info.seafaceColormap)
    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        self.sys_info.seafaceColormap = 'ocean'
        self.plot3d_z_widget.updateColormap(self.sys_info.seafaceColormap)

    @pyqtSlot(int)
    def on_comboBox_activated(self, index):
        self.sys_info.fengji = index+1 
        self.sys_info.seaDataGen.update_para()
        self.plot3d_z_widget.updateStaticView(self.sys_info.seaDataGen.getSeaData()[2])

    def show(self):
        self.move(self.sys_info.desktopWidth*0.15, self.sys_info.desktopHeight*0.15)
        self.resize(self.sys_info.desktopWidth*0.7, self.sys_info.desktopHeight*0.7)  
        super().show()

    def resizeEvent(self,event):
        self.plot3d_z_widget = MayaviQWidget(self.sys_info, self.widget_19, 0)