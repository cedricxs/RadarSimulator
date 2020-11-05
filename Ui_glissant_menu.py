# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\workspace_py\radar\glissant_menu.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Glissant_Menu(object):
    def setupUi(self, Glissant_Menu):
        Glissant_Menu.setObjectName("Glissant_Menu")
        Glissant_Menu.resize(197, 322)
        Glissant_Menu.setMinimumSize(QtCore.QSize(0, 0))
        Glissant_Menu.setMouseTracking(True)
        Glissant_Menu.setStyleSheet("QDialog#Dialog{background-image:url(:/img/image_dialog.jpg);\n"
"border-radius: 20px}")
        Glissant_Menu.setModal(False)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Glissant_Menu)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_2 = QtWidgets.QWidget(Glissant_Menu)
        self.widget_2.setMinimumSize(QtCore.QSize(0, 0))
        self.widget_2.setMaximumSize(QtCore.QSize(20, 999))
        self.widget_2.setStyleSheet("QWidget#widget_2{border-image:url(:/img/image_glissant.png)}")
        self.widget_2.setObjectName("widget_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_3.setGeometry(QtCore.QRect(-10, 0, 31, 321))
        self.pushButton_3.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_3.setStyleSheet(" ")
        self.pushButton_3.setText("")
        self.pushButton_3.setFlat(True)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(Glissant_Menu)
        self.widget.setMouseTracking(True)
        self.widget.setStyleSheet("QWidget#widget{background-image:url(:/img/image_dialog.jpg)}")
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_2.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setMinimumSize(QtCore.QSize(0, 40))
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(11)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_2.addWidget(self.pushButton_2)
        self.checkBox = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_2.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_2.addWidget(self.checkBox_2)
        self.checkBox_3 = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_2.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.widget)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(10)
        self.checkBox_4.setFont(font)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_2.addWidget(self.checkBox_4)
        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(Glissant_Menu)
        QtCore.QMetaObject.connectSlotsByName(Glissant_Menu)

    def retranslateUi(self, Glissant_Menu):
        _translate = QtCore.QCoreApplication.translate
        Glissant_Menu.setWindowTitle(_translate("Glissant_Menu", "Dialog"))
        self.pushButton.setText(_translate("Glissant_Menu", "运行"))
        self.pushButton_2.setText(_translate("Glissant_Menu", "暂停"))
        self.checkBox.setText(_translate("Glissant_Menu", "海浪平面"))
        self.checkBox_2.setText(_translate("Glissant_Menu", "后向散射系数平面"))
        self.checkBox_3.setText(_translate("Glissant_Menu", "杂波统计图"))
        self.checkBox_4.setText(_translate("Glissant_Menu", "多普勒图"))


import img_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Glissant_Menu = QtWidgets.QDialog()
    ui = Ui_Glissant_Menu()
    ui.setupUi(Glissant_Menu)
    Glissant_Menu.show()
    sys.exit(app.exec_())
