from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QPushButton, QLabel, QLineEdit,QTextEdit
from PyQt5.QtGui import QMovie,QIntValidator,QFont
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt as qt

class Ui_MainWindow(object):
    content = 0
    content_2 = 0
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 830)
        MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")

        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(18)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setFont(QFont("Roman times", 18))

        self.textbox = QLabel(MainWindow)
        self.textbox.setAlignment(qt.AlignLeft)
        self.textbox.setAlignment(qt.AlignTop)
        self.textbox.move(30, 600)
        self.textbox.resize(700, 200)
        self.textbox.setFont(QFont("Roman times", 16))
        self.textbox.setStyleSheet("border-width: 3px;border-style: solid ;border-color: rgb(204, 232, 207);")
        self.textbox.setText("帮助：\n左上角的框体是文件显示栏，右上角是文件目录显示栏\n右下角是剩余内存显示栏，左下角是帮助"
                             "文件显示栏内右键展开菜单\n有打开文件/文件夹，删除文件/文件夹，创建文件和文件夹\n"
                             "棕色为文件夹，绿色为文件，只能保存txt格式文件，不需要输入后缀名")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Files Manager"))

    def showtext(self):
        if (self.textbox.text()):
            self.content = self.textbox.text()
        else:
            self.content = 0