from LoadingPage import LoadingPage
from SeafacePage import SeafacePage
from RadarPage import RadarPage
from TargetPage import TargetPage
from MainWindow import MainWindow
from System_Infomations import System_Infomations


from PyQt5 import  QtWidgets

class Application:

    def __init__(self):
        #初始化应用程序
        self.sys_info = System_Infomations()
        self.loadingPage = LoadingPage(self.sys_info)
        self.sys_info.appStatus.addObservateur(self)
        
        #显示加载页面
        self.loadingPage.show()
         
        self.seafacePage = SeafacePage(self.sys_info)
        self.radarPage = RadarPage(self.sys_info)
        self.targetPage = TargetPage(self.sys_info)
        self.mainWindow = MainWindow(self.sys_info)

        self.sys_info.appStatus.set('loadReady')

    def updateView(self,appStatus):
        if appStatus == 'loadReady':
            self.loadingPage.updateView(appStatus)
        elif appStatus == 'seafacePage':
            self.loadingPage.close()  
            self.seafacePage.show()
        elif appStatus == 'radarPage':
            self.seafacePage.close()
            self.radarPage.show()
        elif appStatus == 'targetPage':
            self.radarPage.close()
            self.targetPage.show()
        elif appStatus == 'mainWindow':
            self.targetPage.close()
            self.mainWindow.show()

    def lancer():
        import sys
        app = QtWidgets.QApplication(sys.argv)
        myApp = Application() 
        sys.exit(app.exec_())

Application.lancer()