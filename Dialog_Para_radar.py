from PyQt5 import QtWidgets
from Ui_dialog_para_radar import Ui_Dialog_para_radar
from PyQt5.QtCore import pyqtSlot
class Dialog_para_radar(QtWidgets.QDialog, Ui_Dialog_para_radar):
    
    def __init__(self, sys_info, parent=None):
        super(Dialog_para_radar, self).__init__(parent)
        self.sys_info = sys_info
        self.setupUi(self)
        self.init_para()
        self.setFixedSize( self.width (),self.height ())
    
    def init_para(self):
        self.lineEdit_24.setText(str(self.sys_info.fGHz))
        if self.sys_info.pol == 'vv':
            self.comboBox.setCurrentIndex(0)
        elif self.sys_info.pol == 'hh':
            self.comboBox.setCurrentIndex(1)
        self.lineEdit_25.setText(str(self.sys_info.Psi_raw))
    @pyqtSlot()
    def on_buttonBox_accepted(self):
        """
        Slot documentation goes here.
        """
        self.sys_info.fGHz = float(self.lineEdit_24.text())
        index = self.comboBox.currentIndex()
        if  index == 0: 
            self.sys_info.pol = 'vv'
        else:
            self.sys_info.pol = 'hh'
        self.sys_info.Psi = float(self.lineEdit_25.text())
        self.sys_info.Psi_raw = float(self.lineEdit_25.text())
        self.parent().update_para()
