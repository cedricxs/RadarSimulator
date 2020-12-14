# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5 import  QtWidgets,QtCore
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
from Plot_Widget import Plot_Widget
from Ui_MainWindow import Ui_MainWindow
from Dialog_Para_radar import Dialog_para_radar
from Dialog_Para_env import Dialog_para_env
from Dialog_para_platform import Dialog_para_platform
from Glissant_Menu import Glissant_Menu
#from logDistribution import LogDistribution
from SeaDataGenerator import SeaData
from NRL_SigmaSea import NRL_SigmaSea_Calculeur
from doppler import Doppler
from logReturnRadar import LogReturnRadar
from Mayavi_Widget import MayaviQWidget
from System_Infomations import System_Infomations
from PlotThread import plotStatisticThread, plotDopplerThread, plotMayaviThread 
from FitModel import ModelFitter
import csv
import multiprocessing   
from TargetGenerator import TargetGenertor

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
        self.targetGen = TargetGenertor()
        self.seaDataGen = SeaData(self.sys_info)
        self.nrlDataGen = NRL_SigmaSea_Calculeur(self.sys_info)
        #self.log_normal = LogDistribution(self.sys_info)
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
        #self.glissant_menu = Glissant_Menu(self.sys_info, self)
        #self.glissant_menu.show()
        self.action_7.setEnabled(False)
        
        ################### Connect All Relation of Observer####################
        self.sys_info.timestamp.addObservateur(self.timeEdit)
        self.sys_info.timestamp.addObservateur(self.dialog_para_platform.timeEdit)
        self.sys_info.z.addObservateur(self.plot3d_z_widget)
        self.sys_info.nrl.addObservateur(self.plot3d_nrl_widget)
        ######################触发更新所有视图###########################
        self.sys_info.initialize() 

        #self.pool=multiprocessing.Pool(4)
    #def updateLayout(self):
        
    def setupAllPlotWidget(self):
        
        ####################### RealTime 海杂波数据 Index 0#####################
        self.setupRealTimePlotWidget()
        
        ####################### 多普勒和对数回波强度 Index 4#####################
        self.setupDopplerWidget()
        self.setupLogReturnRadarWidget()
        
        ####################### 海平面和后向散射系数三维图 Index 5#####################
        self.setup3DPlotWidget()
    
    def setupRealTimePlotWidget(self):
        self.plot_widget1 = Plot_Widget(self.widget_14)
        self.plot_widget2 = Plot_Widget(self.widget_15)
        self.plot_widget1.set_facecolor('black')
        self.plot_widget2.set_facecolor('black')
        self.plot_widget1.setPara('real time sea clutter', '', 'Amplitude')
        self.plot_widget2.setPara('Probability Distribution', '', 'Probability Density')

    def setupDopplerWidget(self):
        self.doppler_plot_widget = Plot_Widget(self.widget_22)
        self.doppler_plot_widget.set_facecolor('black')
        self.doppler_plot_widget.setPara('time doppler','m/s', 'Amplitude')
    def setupLogReturnRadarWidget(self):
        self.logReturnRadar_plot_widget = Plot_Widget(self.widget_18)
        self.dopplerRes_widget = self.logReturnRadar_plot_widget
        self.dopplerRes_widget.set_facecolor('black')
        self.dopplerRes_widget.setPara('time doppler','m/s', 'time')

    def setup3DPlotWidget(self):
        #self.plot3d_widget = Plot_Widget3D_Matplt(self.widget_18)
        self.plot3d_z_widget = MayaviQWidget(self.sys_info, self.widget_19, 0)
        self.plot3d_nrl_widget = MayaviQWidget(self.sys_info, self.widget_13, 1)

    def close3DPlotWidget(self):
        self.plot3d_z_widget.close()
        self.plot3d_nrl_widget.close()

    def plot3D(self):
        self.plotMayaviThread = plotMayaviThread(self)
        self.plotMayaviThread.start()
    
    def plotRealtimeStatistic(self):
        #self.plot_widget1.start_animation()
        self.plotStatisticThread = plotStatisticThread(self)
        self.plotStatisticThread.start()
        
    def plotDopplerRealTime(self):
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
        self.startRun()
        
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        self.pauseRun()


    def updateSize(self):
        self.plot3d_z_widget.updateSize()
        self.plot3d_nrl_widget.updateSize()
        self.plot_widget1.resize(self.plot_widget1.parent().size())
        self.plot_widget2.resize(self.plot_widget2.parent().size())
        self.doppler_plot_widget.resize(self.doppler_plot_widget.parent().size())
        self.logReturnRadar_plot_widget.resize(self.logReturnRadar_plot_widget.parent().size())

    def resizeEvent(self, event):
        if self.stackedWidget_2.currentIndex() ==  0:
            self.updateSize()
    
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
    def on_pushButton_6_clicked(self):
        """
        Slot documentation goes here.
        """
        filename = QFileDialog.getSaveFileName(self, "保存数据","sea_clutter_data",  "csv (*.csv);;Text files (*.txt);;XML files (*.xml)")
        if filename[0] != '':
            self.create_csv(filename[0])

    @pyqtSlot()
    def on_pushButton_7_clicked(self):
        """
        Slot documentation goes here.
        """
        self.shutdown()

    def startRun(self):
        self.plotRun = True
        # self.pool.apply_async(self.plot3D())
        # self.pool.apply_async(self.plotRealtimeStatistic())
        # self.pool.apply_async(self.plotDopplerRealTime())
        self.plot3D()
        self.plotRealtimeStatistic()
        self.plotDopplerRealTime()
        self.action_7.setEnabled(True)
        self.action_2.setEnabled(False)
        
    def pauseRun(self):
        self.plotRun = False
        self.action_7.setEnabled(False)
        self.action_2.setEnabled(True)

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
    def on_checkBox_clicked(self):
        if self.checkBox.isChecked() == False:
            self.plot3d_z_widget.parent().setMaximumSize(QtCore.QSize(0, 0))
            self.resize(self.width(),self.height()+1)
            self.checkBox_2.setEnabled(False)
        else:
            self.plot3d_z_widget.parent().setMaximumSize(QtCore.QSize(9999, 9999))
            self.resize(self.width(),self.height()-1)
            self.checkBox_2.setEnabled(True)
    
    @pyqtSlot()
    def on_checkBox_2_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox_2.isChecked() == False:
            self.plot3d_nrl_widget.parent().setMaximumSize(QtCore.QSize(0, 0))
            self.resize(self.width(),self.height()+1)
            self.checkBox.setEnabled(False)
        else:
            self.plot3d_nrl_widget.parent().setMaximumSize(QtCore.QSize(9999, 9999))
            self.resize(self.width(),self.height()-1)
            self.checkBox.setEnabled(True)

    @pyqtSlot()
    def on_checkBox_3_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox_3.isChecked() == False:
            self.verticalLayout_2.setStretch(1,0)
            self.resize(self.width(),self.height()+1)
        else:
            self.verticalLayout_2.setStretch(1,1)
            self.resize(self.width(),self.height()-1)

    @pyqtSlot()
    def on_checkBox_4_clicked(self):
        """
        Slot documentation goes here.
        """
        if self.checkBox_4.isChecked() == False:
            self.horizontalLayout_6.setStretch(0,0)
            self.resize(self.width(),self.height()+1)
        else:
            self.horizontalLayout_6.setStretch(0,1)
            self.resize(self.width(),self.height()-1)

    def lancer():
        import sys
        app = QtWidgets.QApplication(sys.argv)
        mainWindow = MainWindow()
        mainWindow.show()
        # adaptation here
        width, height = QApplication.desktop().width(), QApplication.desktop().height()
        # 先move再resize, 逻辑很重要
        mainWindow.move(width*0.1, height*0.1)
        mainWindow.resize(width*0.8, height*0.8)
        sys.exit(app.exec_())
    
    def shutdown(self):
        self.pauseRun()
        #self.pool.close()
        self.close3DPlotWidget()
        self.close()
