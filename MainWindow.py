# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from Plot_Widget import Plot_Widget, Plot_Widget_QChart
from Ui_MainWindow import Ui_MainWindow
from Dialog_Para_radar import Dialog_para_radar
from Dialog_Para_env import Dialog_para_env
from Dialog_para_platform import Dialog_para_platform
from Glissant_Menu import Glissant_Menu
from logDistribution import LogDistribution
from SeaDataGenertor import SeaData
from NRL_SigmaSea import NRL_SigmaSea_Calculeur
from doppler import Doppler
from logReturnRadar import LogReturnRadar
from Mayavi_Widget import MayaviQWidget
from System_Infomations import System_Infomations
from PlotThread import plotStatisticThread, plotDopplerThread, plotMayaviThread 
from FitModel import ModelFitter
import csv
                
        
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
        #################### setUp All QtDesigner widgets########################
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        #################### setUp system inforamtion########################
        self.sys_info = System_Infomations()
        
        #################### setUp data genertors########################
        self.seaDataGen = SeaData(self.sys_info)
        self.nrlDataGen = NRL_SigmaSea_Calculeur(self.sys_info)
        self.log_normal = LogDistribution(self.sys_info)
        self.doppler = Doppler(self.sys_info)
        self.doppler_count = 0
        self.logReturnRadar = LogReturnRadar(self.sys_info)
        self.modelFitter = ModelFitter()
        self.best_Y_Theorie = None
        #################### setUp All Plot widgets ########################
        #设置无边框
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setupAllPlotWidget()
    
        
        #################### Init default Index########################
        self.stackedWidget_2.setCurrentIndex(5)
        
        #在使用观察者模式后不需要此块
        #################### Init All information labels########################
        self.update_para()
        self.dialog_para_radar = Dialog_para_radar(self.sys_info, self)
        self.dialog_para_env = Dialog_para_env(self.sys_info, self)
        self.dialog_para_platform = Dialog_para_platform(self.sys_info, self)
        self.glissant_menu = Glissant_Menu(self.sys_info, self)
        self.glissant_menu.show()
        self.action_7.setEnabled(False)
        
        ################### Connect All Relation of Observer####################
        self.sys_info.timestamp.addObservateur(self.timeEdit)
        self.sys_info.timestamp.addObservateur(self.dialog_para_platform.timeEdit)
        self.sys_info.z.addObservateur(self.plot3d_z_widget)
        self.sys_info.nrl.addObservateur(self.plot3d_nrl_widget)
        ######################触发更新所有视图###########################
        self.sys_info.initialize() 
    #def updateLayout(self):
        
    def setupAllPlotWidget(self):
        
        ####################### RealTime 海杂波数据 Index 0#####################
        self.plot_widget1 = Plot_Widget(self.widget_14)
        self.plot_widget2 = Plot_Widget(self.widget_15)
        self.plot_widget1.set_facecolor('black')
        self.plot_widget2.set_facecolor('black')
        #self.plot_widget3 = Plot_Widget(self.widget_1)
        
        self.plot_widget1.setPara('real time sea clutter', 'Time', 'Amplitude')
        self.plot_widget2.setPara('Probability Distribution', 'Amplitude', 'Probability Density')
        #self.plot_widget3.setPara('Spectrum', 'Frquency', 'Power Spectral Density')

        ####################### 幅度统计分布模型log分布 Index 1#####################
        self.plot_widget4 = Plot_Widget(self.widget_4)
        self.plot_widget5 = Plot_Widget(self.widget_6)
        self.plot_widget6 = Plot_Widget(self.widget_2)

        self.plot_widget4.setPara('real time sea clutter', 'Time', 'Amplitude')
        self.plot_widget5.setPara('Probability Distribution', 'Amplitude', 'Probability Density')
        self.plot_widget6.setPara('Spectrum', 'Frquency', 'Power Spectral Density')
        ####################### 空 Index 2#####################
        self.plot_widget7 = Plot_Widget(self.widget_7)
        self.plot_widget8 = Plot_Widget(self.widget_8)
        self.plot_widget9 = Plot_Widget(self.widget_9)

        ####################### 空 Index 3#####################
        self.plot_widget10 = Plot_Widget(self.widget_10)
        self.plot_widget11 = Plot_Widget(self.widget_11)
        self.plot_widget12 = Plot_Widget(self.widget_12)
        
        ####################### 多普勒和对数回波强度 Index 4#####################
        self.setupDopplerWidget()
        self.setupLogReturnRadarWidget()
        
        ####################### 海平面和后向散射系数三维图 Index 5#####################
        self.setup3DPlotWidget()
        
    def setupDopplerWidget(self):
        self.doppler_plot_widget = Plot_Widget(self.widget_24)
        self.doppler_plot_widget.set_facecolor('black')
        self.doppler_plot_widget.setPara('time doppler','m/s', 'Amplitude')
    def setupLogReturnRadarWidget(self):
        self.logReturnRadar_plot_widget = Plot_Widget(self.widget_21)
        self.dopplerRes_widget = self.logReturnRadar_plot_widget
        self.dopplerRes_widget.set_facecolor('black')
        self.dopplerRes_widget.setPara('time doppler','m/s', 'time')
    def setup3DPlotWidget(self):
        #self.plot3d_widget = Plot_Widget3D_Matplt(self.widget_18)
        self.plot3d_z_widget = MayaviQWidget(self.sys_info, self.widget_13, 0)
        self.plot3d_nrl_widget = MayaviQWidget(self.sys_info, self.widget_19, 1)
    def close3DPlotWidget(self):
        self.plot3d_z_widget.close()
        self.plot3d_nrl_widget.close()

    def plot3D(self):
        self.plotMayaviThread = plotMayaviThread(self)
        self.plotMayaviThread.start()
    def update_AmStDisModel(self):
        self.stackedWidget_2.setCurrentIndex(1)
        self.plot_widget4.resize(self.plot_widget4.parent().size())
        self.plot_widget5.resize(self.plot_widget5.parent().size())
        self.plot_widget6.resize(self.plot_widget6.parent().size())
        self.log_normal.updateData()
        xaxis, xdata = self.log_normal.xaxis, self.log_normal.xdata
        xaxis1, xpdf1, th_val = self.log_normal.xaxis1, self.log_normal.xpdf1, self.log_normal.th_val
        fre, psd, powerf = self.log_normal.freqx, self.log_normal.psd_dat, self.log_normal.powerf
        self.plot_widget4.updateData([xaxis, xdata])
        self.plot_widget5.updateData([xaxis1, xpdf1, th_val])
        self.plot_widget6.updateData([fre, psd, powerf])   
    
    def plotRealtimeStatistic(self):
        #self.plot_widget1.start_animation()
        self.plotStatisticThread = plotStatisticThread(self)
        self.plotStatisticThread.start()
        
    def plotDopplerRealTime(self):
        self.doppler.calcul(0)
        self.plotDopplerThread = plotDopplerThread(self)
        self.plotDopplerThread.start()
    
    def update_para(self):
        self.lineEdit_22.setText(str(self.sys_info.fGHz))
        if self.sys_info.pol == 'vv':
            self.comboBox.setCurrentIndex(0)
        elif self.sys_info.pol == 'hh':
            self.comboBox.setCurrentIndex(1)
        self.lineEdit_26.setText(str(self.sys_info.Psi_raw))
        if self.sys_info.fengji_changed == True:
            self.lineEdit_11.setText(str(self.sys_info.fengji))
            self.seaDataGen.update_para()
            self.sys_info.fengji_changed = False
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.update_AmStDisModel()
        

    def resizeEvent(self, event):
        if self.stackedWidget_2.currentIndex() ==  0:
           self.plot_widget1.resize(self.plot_widget1.parent().size())
           self.plot_widget2.resize(self.plot_widget2.parent().size())
           #self.plot_widget3.resize(self.plot_widget3.parent().size())
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
            self.plot3d_z_widget.updateSize()
            self.plot3d_nrl_widget.updateSize()
            self.plot_widget1.resize(self.plot_widget1.parent().size())
            self.plot_widget2.resize(self.plot_widget2.parent().size())

    @pyqtSlot()
    def on_action_triggered(self):
        """
        Slot documentation goes here.
        """
        self.dialog_para_radar.show()
    
    @pyqtSlot()
    def on_action_3_triggered(self):
        """
        Slot documentation goes here.
        """
        self.dialog_para_platform.show()
    
    @pyqtSlot()
    def on_action_5_triggered(self):
        """
        Slot documentation goes here.
        """
        self.dialog_para_env.show()
    
    @pyqtSlot()
    def on_pushButton_5_clicked(self):
        """
        Slot documentation goes here.
        """
        self.dialog_para_platform.show()
    
    @pyqtSlot()
    def on_pushButton_4_clicked(self):
        """
        Slot documentation goes here.
        """
        self.dialog_para_radar.show()
    
    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        self.dialog_para_env.show()
    
    @pyqtSlot()
    def on_action_7_triggered(self):
        """
        Slot documentation goes here.
        """
        self.pauseRun()
    
    def startRun(self):
        self.plotRun = True
        self.plot3D()
        self.plotRealtimeStatistic()
        self.action_7.setEnabled(True)
        self.action_2.setEnabled(False)
        
    def pauseRun(self):
        self.plotRun = False
        self.action_7.setEnabled(False)
        self.action_2.setEnabled(True)
    @pyqtSlot()
    def on_action_2_triggered(self):
        """
        Slot documentation goes here.
        """
        self.startRun()
    
    @pyqtSlot()
    def on_action_6_triggered(self):
        """
        Slot documentation goes here.
        """
        filename = QFileDialog.getSaveFileName(self, "保存数据","sea_clutter_data",  "csv (*.csv);;Text files (*.txt);;XML files (*.xml)")
        self.create_csv(filename[0])
    def create_csv(self, filepath):
        if filepath is not None:
            with open(filepath,'w', newline='', encoding='utf-8') as file:
                csv_write = csv.writer(file)
                csv_head_name = self.sys_info.paralist()
                csv_write.writerow(csv_head_name)
                csv_head_value = self.sys_info.valuelist()
                csv_write.writerow(csv_head_value)
                csv_write.writerows([[value] for value in self.nrlDataGen.sample_data])
    
    @pyqtSlot()
    def on_action_4_triggered(self):
        """
        Slot documentation goes here.
        """
        self.stackedWidget_2.setCurrentIndex(5)
    
    @pyqtSlot()
    def on_action_9_triggered(self):
        """
        Slot documentation goes here.
        """
        self.stackedWidget_2.setCurrentIndex(5)
    
    @pyqtSlot()
    def on_action_11_triggered(self):
        """
        Slot documentation goes here.
        """
        self.stackedWidget_2.setCurrentIndex(0)
    
    @pyqtSlot()
    def on_action_13_triggered(self):
        """
        Slot documentation goes here.
        """
        self.stackedWidget_2.setCurrentIndex(4)
        self.doppler_plot_widget.resize(self.doppler_plot_widget.parent().size())
        self.logReturnRadar_plot_widget.resize(self.logReturnRadar_plot_widget.parent().size())
        self.plotDopplerRealTime()
        
    def lancer():
        import sys
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        #mainWindow.resize(880, 600)
        sys.exit(app.exec_())
    
    @pyqtSlot()
    def on_action_8_triggered(self):
        """
        Slot documentation goes here.
        """
        self.pauseRun()
        self.close3DPlotWidget()
        self.close()
