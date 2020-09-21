from PyQt5 import QtWidgets
from Ui_dialog_para_platform import Ui_Dialog_para_platform
from PyQt5.QtCore import pyqtSlot
class Dialog_para_platform(QtWidgets.QDialog, Ui_Dialog_para_platform):
    def __init__(self, sys_info, parent=None):
        super(Dialog_para_platform, self).__init__(parent)
        self.setupUi(self)
        self.sys_info = sys_info
        self.init_para()
        
    def init_para(self):
        self.lineEdit_27.setText(str(self.sys_info.timestamp))
        self.lineEdit_24.setText(str(self.sys_info.jing))
        self.lineEdit_26.setText(str(self.sys_info.wei))
        self.lineEdit_25.setText(str(self.sys_info.height))
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        self.sys_info.timestamp = int(self.lineEdit_27.text())
        self.sys_info.jing = int(self.lineEdit_24.text())
        self.sys_info.wei = int(self.lineEdit_26.text())
        self.sys_info.height = int(self.lineEdit_25.text())
        self.parent().update_para()
