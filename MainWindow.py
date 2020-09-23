# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5 import  QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from Plot_Widget import Plot_Widget
from Ui_MainWindow import Ui_MainWindow
from Dialog_Para_radar import Dialog_para_radar
from Dialog_Para_env import Dialog_para_env
from Dialog_para_platform import Dialog_para_platform
from logDistribution import LogDistribution
from SeaDataGenertor import SeaData
from NRL_SigmaSea import NRL_SigmaSea_Calculeur
from doppler import Doppler
from logReturnRadar import LogReturnRadar
from Mayavi_Widget import MayaviQWidget, Visualization
from System_Infomations import System_Infomations
import numpy as np
import threading
import time
import csv
class plotThread (threading.Thread):   #继承父类threading.Thread
    def __init__(self, parent):
        threading.Thread.__init__(self)
        self.count = 0
        self.parent = parent
    def run(self):                   #把要执行的代码写到run函数里面 线程在创建后会直接运行run函数 
        while self.parent.run == True:
            
            self.count = self.count+1
            xdata = np.array(NRL_SigmaSea_Calculeur.getInstance().sample_data)
            if len(xdata)>0:
                if len(xdata)>100:
                    #最多显示100个点
                    show_data = xdata[len(xdata)-100:]
                    time_seq = range(len(xdata)-100, len(xdata))
                else:
                    show_data = xdata
                    time_seq = range(len(xdata))
                start = time.time()
                self.parent.plot_widget1.updateData([time_seq, show_data])
                print("time plot:"+str(time.time()-start))
                if self.count%5 == 0:
                    maxdat, mindat = max(xdata), min(xdata)
                    if maxdat != mindat:
                        xaixs = np.arange(mindat, maxdat+(maxdat-mindat)/10, (maxdat-mindat)/10)
                        xpdf = np.histogram(xdata, xaixs, density=True)[0]
                        xpdf = np.append(xpdf, [0])
                        self.parent.plot_widget2.updateData([xaixs, xpdf])
            
            
            time.sleep(0.8)
                
        
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
        self.sys_info = System_Infomations()
        
        self.seaDataGen = SeaData(self.sys_info)
        self.nrlDataGen = NRL_SigmaSea_Calculeur(self.sys_info)
        self.log_normal = LogDistribution(self.sys_info)
        self.doppler = Doppler(self.sys_info)
        self.doppler_count = 0
        self.logReturnRadar = LogReturnRadar(self.sys_info)
        
        #self.setWindowFlags(Qt.FramelessWindowHint)
        self.setup2DPlotWidget()
        self.setup3DPlotWidget()
        self.setupDopplerWidget()
        self.setupLogReturnRadarWidget()
        
        self.plot_widget1.setPara('real time sea clutter', 'Time', 'Amplitude')
        self.plot_widget2.setPara('Probability Distribution', 'Amplitude', 'Probability Density')
        self.plot_widget3.setPara('Spectrum', 'Frquency', 'Power Spectral Density')
        
        
        self.stackedWidget_2.setCurrentIndex(5)
        Visualization.plotStatus = 0
        self.plot3d_widget.visualization.plot_static()
        self.plot3d_widget.updateSize()
        self.radioButton_9.setChecked(True)
        self.update_para()
        self.dialog_para_radar = Dialog_para_radar(self.sys_info, self)
        self.dialog_para_env = Dialog_para_env(self.sys_info, self)
        self.dialog_para_platform = Dialog_para_platform(self.sys_info, self)
        self.action_7.setEnabled(False)
    
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
        self.plot3d_widget = MayaviQWidget(self.sys_info, self.widget_19)
        
    def plot3D(self):
        self.animation = Visualization.animation()
    def update(self):
        if self.stackedWidget_2.currentIndex() ==  0:
            self.log_normal.updateData()
            xaxis1, xpdf1, th_val = self.log_normal.xaxis1, self.log_normal.xpdf1, self.log_normal.th_val
            fre, psd, powerf = self.log_normal.freqx, self.log_normal.psd_dat, self.log_normal.powerf
            self.plot_widget2.updateData([xaxis1, xpdf1, th_val])
            self.plot_widget3.updateData([fre, psd, powerf])   
        else:
            pass
    
    def plotRealtime(self):
        self.run = True
        #self.plot_widget1.start_animation()
        self.plotThread = plotThread(self)
        self.plotThread.start()
    
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
        self.lineEdit_2.setText(str(self.sys_info.timestamp))
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.update()
        

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
    def on_radioButton_7_clicked(self):
        """
        Slot documentation goes here.
        """
        #if self.radioButton.isChecked():
        self.stackedWidget_2.setCurrentIndex(0)
        #elif self.radioButton_2.isChecked():
        #self.stackedWidget_2.setCurrentIndex(1)
        #elif self.radioButton_3.isChecked():
        #self.stackedWidget_2.setCurrentIndex(3)
        
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.plot3D()
        self.plotRealtime()
    
    @pyqtSlot()
    def on_radioButton_9_clicked(self):
        """
        Slot documentation goes here.
        """
        self.stackedWidget_2.setCurrentIndex(5)
        Visualization.plotStatus = 0
        self.plot3d_widget.visualization.plot_static()
        self.plot3d_widget.updateSize()
    
    @pyqtSlot()
    def on_radioButton_10_clicked(self):
        """
        Slot documentation goes here.
        """
        self.stackedWidget_2.setCurrentIndex(5)
        Visualization.plotStatus = 1
        self.plot3d_widget.visualization.plot_static()
        self.plot3d_widget.updateSize()
    

    
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
        self.logReturnRadar_plot_widget.resize(self.logReturnRadar_plot_widget.parent().size())
    
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
        self.run = False
        self.animation.stop = True
        self.action_7.setEnabled(False)
        self.action_2.setEnabled(True)
    
    @pyqtSlot()
    def on_action_2_triggered(self):
        """
        Slot documentation goes here.
        """
        self.plot3D()
        self.plotRealtime()
        self.action_7.setEnabled(True)
        self.action_2.setEnabled(False)
    
    @pyqtSlot()
    def on_action_6_triggered(self):
        """
        Slot documentation goes here.
        """
        filename = QFileDialog.getSaveFileName(self, "保存数据","sea_clutter_data",  "csv (*.csv);;Text files (*.txt);;XML files (*.xml)")
        self.create_csv(filename[0])
    
    def create_csv(self, filepath):
        with open(filepath,'w', newline='', encoding='utf-8') as file:
            csv_write = csv.writer(file)
            csv_head_name = self.sys_info.paralist()
            csv_write.writerow(csv_head_name)
            csv_head_value = self.sys_info.valuelist()
            csv_write.writerow(csv_head_value)
            csv_write.writerows([[value] for value in self.plot3d_widget.visualization.nRL_SigmaSea_Calculeur.sample_data])
