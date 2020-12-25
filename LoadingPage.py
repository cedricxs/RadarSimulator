from PyQt5 import QtWidgets
from Ui_loadingPage import Ui_Form
from PyQt5.QtCore import pyqtSlot, Qt 
class LoadingPage(QtWidgets.QWidget, Ui_Form):
    
    def __init__(self, sys_info, parent=None):
        super(LoadingPage, self).__init__(parent)
        self.setupUi(self)
        self.sys_info = sys_info
        self.setWindowFlags(Qt.FramelessWindowHint)
        # 先move再resize, 逻辑很重要
        width, height = self.sys_info.desktopWidth, self.sys_info.desktopHeight
        self.move(width*0.2, height*0.2)
        self.resize(width*0.6, height*0.6)

    def updateView(self,appStatus):
        if appStatus == 'loadReady':
            self.label_6.setText('动态模拟器已加载成功 请开始......')
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        self.sys_info.appStatus.set('seafacePage')
    