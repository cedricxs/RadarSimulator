from PyQt5 import QtWidgets
from Ui_dialog_para_env import Ui_Dialog_para_env
from PyQt5.QtCore import pyqtSlot
class Dialog_para_env(QtWidgets.QDialog, Ui_Dialog_para_env):
    def __init__(self, sys_info, parent=None):
        super(Dialog_para_env, self).__init__(parent)
        self.setupUi(self)
        self.sys_info = sys_info
        self.init_para()
        self.setFixedSize( self.width (),self.height ())
        
    def init_para(self):
        self.lineEdit_24.setText(str(self.sys_info.fengji))
        
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        self.sys_info.fengji = int(self.lineEdit_24.text())
        self.sys_info.fengji_changed = True
        self.parent().update_para()
