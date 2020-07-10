# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QMainWindow
from Plot_Widget import Plot_Widget, Plot_Widget3D_Matplt
from Ui_MainWindow import Ui_MainWindow
from logDistribution import LogDistribution
import numpy as np
from doppler import Doppler
from logReturnRadar import LogReturnRadar
from Mayavi_Widget import MayaviQWidget, Visualization
class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setup2DPlotWidget()
        self.setup3DPlotWidget()
        self.setupDopplerWidget()
        self.setupLogReturnRadarWidget()
        self.log_normal = LogDistribution()
        self.doppler = Doppler()
        self.doppler_count = 0
        self.logReturnRadar = LogReturnRadar()
        self.stackedWidget_2.setCurrentIndex(0)
        self.radioButton.setChecked(True)
        self.radioButton_7.setChecked(True)
        self.dynSystemeData()
    
    def setup2DPlotWidget(self):
        
        ####################### log分布 #####################
        self.plot_widget1 = Plot_Widget(self.widget_5)
        self.plot_widget2 = Plot_Widget(self.widget_1)
        self.plot_widget3 = Plot_Widget(self.widget)
        
        ####################### 瑞利分布 #####################
        self.plot_widget4 = Plot_Widget(self.widget_6)
        self.plot_widget5 = Plot_Widget(self.widget_2)
        self.plot_widget6 = Plot_Widget(self.widget_4)

        ####################### k分布 #####################
        self.plot_widget7 = Plot_Widget(self.widget_7)
        self.plot_widget8 = Plot_Widget(self.widget_8)
        self.plot_widget9 = Plot_Widget(self.widget_9)

        ####################### 韦伯尔分布 #####################
        self.plot_widget10 = Plot_Widget(self.widget_10)
        self.plot_widget11 = Plot_Widget(self.widget_11)
        self.plot_widget12 = Plot_Widget(self.widget_12)
        
    def setupDopplerWidget(self):
        self.doppler_plot_widget = Plot_Widget(self.widget_24)
    def setupLogReturnRadarWidget(self):
        self.logReturnRadar_plot_widget = Plot_Widget(self.widget_21)
    def setup3DPlotWidget(self):
        #self.plot3d_widget = Plot_Widget3D_Matplt(self.widget_18)
        self.plot3d_widget = MayaviQWidget(self.widget_19)
        pass
        
    def plot3D(self):
        #x, y = np.meshgrid(np.arange(-2, 2, 0.05),  np.arange(-2, 2, 0.05))
        #z = x*np.exp(-x**2-y**2)
        #self.plot3d_widget.updateData([x, y, z])
        #self.plot3d_widget.visualization.plot()
        self.plot3d_widget.visualization.animation()
    
    def dynSystemeData(self):
        self.lineEdit_22.setText(str(Visualization.nRL_SigmaSea_Calculeur.fGHz))
        if Visualization.nRL_SigmaSea_Calculeur.Pol == 'V':
            self.comboBox.setCurrentIndex(0)
        else:
            self.comboBox.setCurrentIndex(1)
        self.lineEdit_26.setText(str(Visualization.nRL_SigmaSea_Calculeur.Psi))
        self.lineEdit_11.setText(str(Visualization.seaData.fengji))
    def update(self):
        if self.stackedWidget_2.currentIndex() ==  0:
            self.log_normal.updateData()
            xdata = self.log_normal.xdata
            xaxis1, xpdf1, th_val = self.log_normal.xaxis1, self.log_normal.xpdf1, self.log_normal.th_val
            fre, psd, powerf = self.log_normal.freqx, self.log_normal.psd_dat, self.log_normal.powerf
            self.plot_widget1.updateData(xdata, 'Log-normal Distribution time Domaine', 'Time', 'Amplitude')
            self.plot_widget2.updateData([xaxis1, xpdf1, th_val],  'Probability Distribution', 'Amplitude', 'Probability Density')
            self.plot_widget3.updateData([fre, psd, powerf], 'Spectrum', 'Frquency', 'Power Spectral Density')
        else:
            pass
    
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.update()
    
    @pyqtSlot()
    def on_lineEdit_editingFinished(self):
        """
        Slot documentation goes here.
        """
        print(self.lineEdit.text())
    
    @pyqtSlot()
    def on_lineEdit_2_editingFinished(self):
        """
        Slot documentation goes here.
        """
        self.log_normal.setMuc(float(self.lineEdit_2.text()))

    def resizeEvent(self, event):
        if self.stackedWidget_2.currentIndex() ==  0:
           self.plot_widget1.resize(self.plot_widget1.parent().size())
           self.plot_widget2.resize(self.plot_widget2.parent().size())
           self.plot_widget3.resize(self.plot_widget3.parent().size())
        elif self.stackedWidget_2.currentIndex() ==  1:
           self.plot_widget4.resize(self.plot_widget4.parent().size())
           self.plot_widget5.resize(self.plot_widget5.parent().size())
           self.plot_widget6.resize(self.plot_widget6.parent().size())
        elif self.stackedWidget_2.currentIndex() ==  2:
           self.plot_widget7.resize(self.plot_widget7.parent().size())
           self.plot_widget8.resize(self.plot_widget8.parent().size())
           self.plot_widget9.resize(self.plot_widget9.parent().size())
        elif self.stackedWidget_2.currentIndex() ==  3:
           self.plot_widget10.resize(self.plot_widget10.parent().size())
           self.plot_widget11.resize(self.plot_widget11.parent().size())
           self.plot_widget12.resize(self.plot_widget12.parent().size())
        elif self.stackedWidget_2.currentIndex() ==  4:
            self.doppler_plot_widget.resize(self.doppler_plot_widget.parent().size())
        elif self.stackedWidget_2.currentIndex() ==  5:
            self.plot3d_widget.updateSize()
    def lancer():
        import sys
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        #mainWindow.resize(880, 600)
        sys.exit(app.exec_())
    
    @pyqtSlot()
    def on_radioButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.radioButton_7.isChecked():
            self.stackedWidget_2.setCurrentIndex(2)
            self.plot_widget7.resize(self.plot_widget7.parent().size())
            self.plot_widget8.resize(self.plot_widget8.parent().size())
            self.plot_widget9.resize(self.plot_widget9.parent().size())
    
    @pyqtSlot()
    def on_radioButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.radioButton_7.isChecked():
            self.stackedWidget_2.setCurrentIndex(1)
            self.plot_widget4.resize(self.plot_widget4.parent().size())
            self.plot_widget5.resize(self.plot_widget5.parent().size())
            self.plot_widget6.resize(self.plot_widget6.parent().size())
    
    @pyqtSlot()
    def on_radioButton_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.radioButton_7.isChecked():
            self.stackedWidget_2.setCurrentIndex(0)
            self.plot_widget1.resize(self.plot_widget1.parent().size())
            self.plot_widget2.resize(self.plot_widget2.parent().size())
            self.plot_widget3.resize(self.plot_widget3.parent().size())

    
    @pyqtSlot()
    def on_radioButton_7_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.radioButton.isChecked():
            self.stackedWidget_2.setCurrentIndex(0)
        elif self.radioButton_2.isChecked():
            self.stackedWidget_2.setCurrentIndex(1)
        elif self.radioButton_3.isChecked():
            self.stackedWidget_2.setCurrentIndex(3)
        
    
    @pyqtSlot()
    def on_radioButton_8_clicked(self):
        """
        Slot documentation goes here.
        """
        self.stackedWidget_2.setCurrentIndex(5)
        self.radioButton_9.setChecked(True)
        self.plot3d_widget.updateSize()
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.plot3D()
    
    @pyqtSlot()
    def on_radioButton_9_clicked(self):
        """
        Slot documentation goes here.
        """
        self.plot3d_widget.visualization.plotStatus = 0
        self.plot3d_widget.visualization.plot_static()
    
    @pyqtSlot()
    def on_radioButton_10_clicked(self):
        """
        Slot documentation goes here.
        """
        self.plot3d_widget.visualization.plotStatus = 1
        self.plot3d_widget.visualization.plot_static()
    
    @pyqtSlot(str)
    def on_lineEdit_11_textChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        Visualization.seaData.fengji = int(p0)
    
    @pyqtSlot(str)
    def on_lineEdit_22_textChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        Visualization.nRL_SigmaSea_Calculeur.fGHz =  int(p0)
    
    @pyqtSlot(int)
    def on_comboBox_currentIndexChanged(self, index):
        """
        Slot documentation goes here.
        
        @param index DESCRIPTION
        @type int
        """
        if  index == 0: 
            Visualization.nRL_SigmaSea_Calculeur.Pol = 'V'
        else:
            Visualization.nRL_SigmaSea_Calculeur.Pol = 'H'
        print(Visualization.nRL_SigmaSea_Calculeur.Pol)
    
    @pyqtSlot(str)
    def on_lineEdit_26_textChanged(self, p0):
        """
        Slot documentation goes here.
        
        @param p0 DESCRIPTION
        @type str
        """
        Visualization.nRL_SigmaSea_Calculeur.Psi = int(p0)
    
    @pyqtSlot()
    def on_pushButton_8_clicked(self):
        """
        Slot documentation goes here.
        """
        x, y, z = self.doppler.calcul(self.doppler_count)
        self.doppler_plot_widget.draw_doppler(x, y, z, self.doppler_count)
        if self.doppler_count == 0:
            x, y, z = self.logReturnRadar.calcul()
            self.logReturnRadar_plot_widget.draw_logReturnRadar(x, y, z)
        self.doppler_count += 1
        if self.doppler_count ==14:
            self.doppler_count = 0
        
    
    @pyqtSlot()
    def on_radioButton_11_clicked(self):
        """
        Slot documentation goes here.
        """
        self.stackedWidget_2.setCurrentIndex(4)
        self.doppler_plot_widget.resize(self.doppler_plot_widget.parent().size())
