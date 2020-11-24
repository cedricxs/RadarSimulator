from PyQt5 import QtWidgets, QtCore
from Ui_glissant_menu import Ui_Glissant_Menu
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui  import QRegion
 
class Glissant_Menu(QtWidgets.QDialog, Ui_Glissant_Menu):
    def __init__(self, sys_info, parent=None):
        super(Glissant_Menu, self).__init__(parent)
        self.setupUi(self)
        self.sys_info = sys_info
        self.init_para()
        self.status = 0
        
    def adjust(self):
        parent_geometry = self.parent().geometry()
        self.setGeometry(parent_geometry.x()+parent_geometry.width()-self.width()*0.15, parent_geometry.y()+parent_geometry.height()/3, 200, 300)
        self.setMask(QRegion(0, 0, self.width()*0.15, self.height()))

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
    def on_commandLinkButton_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.status == 0:
            self.moveIn()
        elif self.status == 1:
            self.moveOut()
    
    @pyqtSlot()
    def on_checkBox_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox.isChecked() == False:
            self.parent().plot3d_z_widget.parent().setMaximumSize(QtCore.QSize(0, 0))
            self.parent().updateSize()
        else:
            self.parent().plot3d_z_widget.parent().setMaximumSize(QtCore.QSize(9999, 9999))
            self.parent().updateSize()

    @pyqtSlot()
    def on_checkBox_2_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox_2.isChecked() == False:
            self.parent().plot3d_nrl_widget.parent().setMaximumSize(QtCore.QSize(0, 0))
            self.parent().resize(self.parent().width(),self.parent().height()+1)
        else:
            self.parent().plot3d_nrl_widget.parent().setMaximumSize(QtCore.QSize(9999, 9999))
            self.parent().resize(self.parent().width(),self.parent().height()-1)

    @pyqtSlot()
    def on_checkBox_3_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox_3.isChecked() == False:
            self.parent().plot_widget1.parent().parent().setMaximumSize(QtCore.QSize(0, 0))
            self.parent().resize(self.parent().width(),self.parent().height()+1)
        else:
            self.parent().plot_widget1.parent().parent().setMaximumSize(QtCore.QSize(9999, 9999))
            self.parent().resize(self.parent().width(),self.parent().height()-1)

    @pyqtSlot()
    def on_checkBox_4_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox_4.isChecked() == False:
            self.parent().doppler_plot_widget.parent().parent().setMaximumSize(QtCore.QSize(0, 0))
            self.parent().resize(self.parent().width(),self.parent().height()+1)
        else:
            self.parent().doppler_plot_widget.parent().parent().setMaximumSize(QtCore.QSize(9999, 9999))
            self.parent().resize(self.parent().width(),self.parent().height()-1)

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
        while parent_geometry.x()+parent_geometry.width() > self.x()+self.width()*0.17:
            self.move(self.x()+15, self.y())
            region = self.mask()
            rect = region.boundingRect()
            rect.setWidth(rect.width()-15)
            print(rect.width())
            self.setMask(QRegion(rect))
        self.status = 0
