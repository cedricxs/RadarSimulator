from PyQt5 import QtWidgets 
from Ui_glissant_menu import Ui_Glissant_Menu
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui  import QRegion
 
class Glissant_Menu(QtWidgets.QDialog, Ui_Glissant_Menu):
    def __init__(self, sys_info, parent=None):
        super(Glissant_Menu, self).__init__(parent)
        self.setupUi(self)
        self.sys_info = sys_info
        self.init_para()
        parent_geometry = self.parent().geometry()
        self.setGeometry(parent_geometry.x()+parent_geometry.width()-40, parent_geometry.y()+parent_geometry.height()/3, 197, 322)
        self.setMask(QRegion(0, 0, 35, self.height()))
        self.showAll = False
        self.status = 0
        
    def init_para(self):
        pass
        
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.parent().startRun()
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.parent().pauseRun()
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.status == 0:
            self.moveIn()
        elif self.status == 1:
            self.moveOut()
    def moveIn(self):
        parent_geometry = self.parent().geometry()
        while parent_geometry.x()+parent_geometry.width() < self.x()+self.width():
            self.move(self.x()-15, self.y())
            region = self.mask()
            rect = region.boundingRect()
            rect.setWidth(rect.width()+15)
            self.setMask(QRegion(rect))
        self.status = 1
    def moveOut(self):
        parent_geometry = self.parent().geometry()
        while parent_geometry.x()+parent_geometry.width() > self.x()+55:
            self.move(self.x()+15, self.y())
            region = self.mask()
            rect = region.boundingRect()
            rect.setWidth(rect.width()-15)
            print(rect.width())
            self.setMask(QRegion(rect))
        self.status = 0
