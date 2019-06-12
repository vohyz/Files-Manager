import os
import sip
import sys
from functools import partial
from functools import partial
from PyQt5 import QtWidgets,QtCore,QtGui,Qt
from PyQt5.QtWidgets import QListWidget,QListWidgetItem
from PyQt5.QtGui import QMovie,QIntValidator,QFont,QCursor,QColor
from PyQt5.QtCore import Qt as qt
from PyQt5.Qt import QMenu,QAction,QSize
from Interface import Ui_MainWindow

store = [[] for i in range(30)]         #模拟内存块
List = ["Home"]                         #总文件索引
ppge = []                               #当前所在位置索引
maxsize = 20                            #内存块最大容量
load = []
dirlist =""
number = 0

class myWindow(QtWidgets.QMainWindow):  #UI界面类
    Name = [i for i in range(20)]
    filepointer = 0
    def __init__(self):
        super(myWindow, self).__init__()
        self.myCommand = " "
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.widget = QtWidgets.QListWidget(self.ui.centralwidget)
        self.ui.widget.setGeometry(QtCore.QRect(30, 50, 700,500))
        self.ui.widget.setStyleSheet("QListWidget{border-width: 3px;border-style: solid ;border-color: rgb(204, 232, 207);}"
                                     "QListWidget::Item{height:100px;width:670px;padding-bottom:10px;}"
                        "QListWidget::Item:hover{border-width:0px;background:skyblue; }"
                        "QListWidget::item:selected:!active{border-width:0px; background:lightgreen; }")
        self.ui.widget.setObjectName("widget")
        self.ui.widget.setContextMenuPolicy(3)
        self.ui.widget.customContextMenuRequested[QtCore.QPoint].connect(self.rightMenuShow)

        self.dirlabel = QtWidgets.QLabel(self.ui.centralwidget)
        self.dirlabel.setGeometry(QtCore.QRect(30, 20, 700, 30))
        self.dirlabel.setFont(QFont("Roman times", 16))

        self.returnbutton = QtWidgets.QPushButton(self.ui.centralwidget)
        self.returnbutton.setGeometry(QtCore.QRect(680, 510, 50, 40))
        self.returnbutton.setStyleSheet("border-width: 1px;border-style: solid ;border-color: rgb(0, 0, 0);")
        self.returnbutton.setText("返回")
        self.returnbutton.clicked.connect(self.ReturnDir)

        self.ui.label = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.label.setGeometry(QtCore.QRect(30, 600, 700, 200))
        self.ui.label.setStyleSheet("border-width: 3px;border-style: solid ;border-color: rgb(204, 232, 207);")
        self.ui.label.setObjectName("label_400")

        self.ui.label_200 = QtWidgets.QLabel(self.ui.centralwidget)
        self.ui.label_200.setAlignment(qt.AlignLeft)
        self.ui.label_200.setAlignment(qt.AlignTop)
        self.ui.label_200.setFont(QFont("Roman times", 16, QFont.Bold))
        self.ui.label_200.setGeometry(QtCore.QRect(780, 50, 300, 500))
        self.ui.label_200.setStyleSheet("border-width: 3px;border-style: solid ;border-color: rgb(204, 232, 207);")
        self.ui.label_200.setObjectName("label_300")

        self.topFiller = QtWidgets.QWidget()
        self.topFiller.setStyleSheet("border-width: 0px;")
        self.topFiller.setMinimumSize(270, 650)
        self.scrolll = QtWidgets.QScrollArea(self.ui.centralwidget)
        self.scrolll.setGeometry(QtCore.QRect(780, 600, 300, 200))
        self.scrolll.setStyleSheet("border-width: 3px;border-style: solid ;border-color: rgb(204, 232, 207);")

        self.ShowStores()

        self.inputname = QtWidgets.QWidget(self.ui.centralwidget)
        self.inputname.setFont(QFont("Roman times", 16, QFont.Bold))
        self.inputname.setGeometry(QtCore.QRect(30, 50, 700, 500))

        self.nameedit1 = QtWidgets.QLineEdit(self.inputname)
        self.nameedit1.setGeometry(QtCore.QRect(275, 220, 150, 40))
        self.nameedit1.setStyleSheet("border-width: 1px;border-style: solid ;border-color: rgb(0, 0, 0);")
        self.nameok = QtWidgets.QPushButton(self.inputname)
        self.nameok.setGeometry(QtCore.QRect(275, 270, 60, 30))
        self.nameok.setText("确认")
        self.nameok.clicked.connect(partial(self.OK,0))
        self.nameend = QtWidgets.QPushButton(self.inputname)
        self.nameend.setGeometry(QtCore.QRect(365, 270, 60, 30))
        self.nameend.setText("取消")
        self.nameend.clicked.connect(partial(self.END,0))
        self.inputname.setHidden(True)

        self.inputfilename = QtWidgets.QWidget(self.ui.centralwidget)
        self.inputfilename.setFont(QFont("Roman times", 16, QFont.Bold))
        self.inputfilename.setGeometry(QtCore.QRect(30, 50, 700, 500))

        self.nameedit2 = QtWidgets.QLineEdit(self.inputfilename)
        self.nameedit2.setGeometry(QtCore.QRect(275, 220, 150, 40))
        self.nameedit2.setStyleSheet("border-width: 1px;border-style: solid ;border-color: rgb(0, 0, 0);")
        self.nameok = QtWidgets.QPushButton(self.inputfilename)
        self.nameok.setGeometry(QtCore.QRect(275, 270, 60, 30))
        self.nameok.setText("确认")
        self.nameok.clicked.connect(partial(self.OK,1))
        self.nameend = QtWidgets.QPushButton(self.inputfilename)
        self.nameend.setGeometry(QtCore.QRect(365, 270, 60, 30))
        self.nameend.setText("取消")
        self.nameend.clicked.connect(partial(self.END,1))
        self.inputfilename.setHidden(True)

        self.FileWindow = QtWidgets.QWidget(self.ui.centralwidget)
        self.FileWindow.setFont(QFont("Roman times", 16, QFont.Bold))
        self.FileWindow.setGeometry(QtCore.QRect(30, 50, 700, 500))
        self.textbox = QtWidgets.QTextEdit(self.FileWindow)
        self.textbox.move(30, 20)
        self.textbox.resize(640, 400)
        self.textbox.setStyleSheet("border-width: 1px;border-style: solid ;border-color: rgb(0, 0, 0);")
        self.textbox.setFont(QFont("Roman times", 16))
        self.nameok = QtWidgets.QPushButton(self.FileWindow)
        self.nameok.setGeometry(QtCore.QRect(80, 440, 120, 60))
        self.nameok.setText("保存文件")
        self.nameok.clicked.connect(self.StoreFile)
        self.nameend = QtWidgets.QPushButton(self.FileWindow)
        self.nameend.setGeometry(QtCore.QRect(500, 440, 120, 60))
        self.nameend.setText("取消编辑")
        self.nameend.clicked.connect(partial(self.END, 2))
        self.FileWindow.setHidden(True)
        self.Load()
        self.Refresh()
        self.ShowDir()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.Store()

    def showdirinUI(self):
        self.ui.label.setText(dirlist)

    def rightMenuShow(self):
        rightMenu = QMenu()
        removeAction = Qt.QAction(u"删除", self,
                                     triggered=self.DeleteDir)  # triggered 为右键菜单点击后的激活事件。这里slef.close调用的是系统自带的关闭事件。
        gotoAction = Qt.QAction(u"打开", self,
                                  triggered=self.GotoDir)  # triggered 为右键菜单点击后的激活事件。这里slef.close调用的是系统自带的关闭事件。
        addAction = Qt.QAction(u"创建文件夹", self,triggered=self.CreateDir)  # 也可以指定自定义对象事件
        addfileAction = Qt.QAction(u"创建文件", self, triggered=self.CreateFile)  # 也可以指定自定义对象事件
        rightMenu.addAction(gotoAction)
        rightMenu.addAction(addAction)
        rightMenu.addAction(addfileAction)
        rightMenu.addAction(removeAction)
        rightMenu.exec_(QtGui.QCursor.pos())

    def Deleteall(self):  # 格式化
        store.clear()
        if os.path.exists("List.txt"):  # 删本地文件
            os.remove("List.txt")

    def InputName(self,NO):
        if NO == 0:
            self.inputname.setHidden(False)
        else:
            self.inputfilename.setHidden(False)

    def StoreFile(self):
        self.content = self.textbox.toPlainText()
        path = self.GetPath()
        self.count = 0
        for i in path[self.filepointer][2:]:
            store[int(i)].clear()
            for j in range(10):
                if self.count<len(self.content):
                    store[int(i)].append(self.content[self.count])
                    self.count += 1
                else:
                    break
        while self.count<len(self.content):
            manager = self.Manager()      #这里必须用一个变量来存Manager返回的值，否则后面每次存入内存后进行的Manager会返回不同目录
            if manager != -1:
                path[self.filepointer].append(manager)
                for i in range(10):
                    if self.count < len(self.content):
                        store[manager].append(self.content[self.count])
                        self.count += 1
                    else:
                        break
            else:
                print("空间已满")
                break
        self.count = 0
        for i in path[self.filepointer][2:]:
            self.count += 1
            if len(store[int(i)]):
                continue
            else:
                length = len(path[self.filepointer])
                for j in range(length-self.count-1):
                    path[self.filepointer].pop()
        self.ShowFiles()
        self.FileWindow.setHidden(True)
        self.Refresh()
        return True

    def OK(self,NO):
        if NO == 0:
            self.content = self.nameedit1.text()
            a = []
            a.append(self.content)
            path = self.GetPath()
            for i in range(1, len(path)):
                if path[i][0] == self.content:
                    return
            for i in range(1, len(path)):
                if len(path[i])>1:
                    if path[i][1] == self.content:
                        return
            path.append(a)
            self.ShowDir()
            self.inputname.setHidden(True)
            return True
        else:
            self.content = self.nameedit2.text()
            a = []
            a.append("FILE")
            a.append(self.content)
            manager = self.Manager()
            if manager != -1:
                store[manager].append(1)
            a.append(manager)
            path = self.GetPath()
            for i in range(1, len(path)):
                if path[i][0] == self.content:
                    return
            for i in range(1, len(path)):
                if len(path[i])>1:
                    if path[i][1] == self.content:
                        return
            path.append(a)
            self.ShowDir()
            self.Refresh()
            self.inputfilename.setHidden(True)
            return True

    def END(self,NO):
        if NO == 0:
            self.inputname.setHidden(True)
        elif NO == 1:
            self.inputfilename.setHidden(True)
        else:
            self.FileWindow.setHidden(True)
        return False

    def EveryDir(self,f,name):
        temp = List
        self.everydir(temp,f,0,name)

    def everydir(self,temp, f,m, name):  # 递归查找文件夹
        for i in range(len(temp)):
            l = m
            if isinstance(temp[i], list):
                if temp[i][0] == "FILE":
                    continue
                else:
                    l += 1
                    if l == int(f) and temp[i][0] == name:
                        self.ppath = temp[i]
                    else:
                        if l >= int(f):
                            continue
                        else:
                            self.everydir(temp[i],f,l,name)

    def Load(self):  # 初始化（从本地文件）
        #恢复文件列表
        if os.path.exists("List.txt"):
            with open("List.txt", "r") as f:
                for s in f:
                    s = s.split()
                    load.append(s)

        for i in range(len(load)):
            if int(load[i][0]) == 1:
                if load[i][1] == '+':
                    a = []
                    a.append(load[i][2])

                    List.append(a)
                else:
                    a = []
                    a.append("FILE")
                    a.append(load[i][2])
                    for m in load[i][3:]:
                        a.append(m)

                    List.append(a)

            if int(load[i][0]) >= int(load[i - 1][0]):
                floor = i
                while floor > 0:
                    floor -= 1
                    if int(load[floor][0]) == int(load[i][0]) - 1:
                        self.EveryDir(load[floor][0], load[floor][2])
                        path = self.ppath
                        if load[i][1] == '+':
                            a = []
                            a.append(load[i][2])
                            path.append(a)
                            break
                        else:
                            a = []
                            a.append("FILE")
                            a.append(load[i][2])
                            for m in load[i][3:]:
                                a.append(m)
                            path.append(a)
                            break
        #恢复内存
        if os.path.exists("Store.txt"):
            with open("Store.txt", "r") as S:
                count = 0
                for s in S:
                    if count < 30:
                        s = s.split()
                        for j in s:
                            store[count].append(j)
                    count += 1

    def ShowStores(self):
        self.Storelist = [[] for i in range(30)]
        for i in range(30):
            label = QtWidgets.QLabel(self.topFiller)
            label.setGeometry(QtCore.QRect(0, i * 21, 20, 20))
            label.setStyleSheet("border:0px;background:white")
            label.setText(str(i))
            for j in range(1,11):
                label1 = QtWidgets.QLabel(self.topFiller)
                label1.setGeometry(QtCore.QRect(j * 21, i * 21, 20, 20))
                label1.setStyleSheet("border:0px;background:lightgreen;")
                label1.setText("")
                self.Storelist[i].append(label1)
        self.scrolll.setWidget(self.topFiller)

    def ReturnDir(self):
        if len(ppge):
            ppge.pop()
        self.ShowFiles()

    def Refresh(self):
        for i in range(30):
            length = len(store[i])
            if length:
                for j in range(length):
                    self.Storelist[i][j].setStyleSheet("border:0px;background:red;")
                for j in range(length,10):
                    self.Storelist[i][j].setStyleSheet("border:0px;background:lightgreen;")
            else:
                for j in range(10):
                    self.Storelist[i][j].setStyleSheet("border:0px;background:lightgreen;")


    def ShowFiles(self):
        path = self.GetPath()
        self.ui.widget.clear()
        for i in range(len(path)-1):
            layout = QtWidgets.QHBoxLayout()
            label = QtWidgets.QLabel()
            label.setFont(QFont("Roman times", 16))
            label.setAlignment(qt.AlignCenter)
            label2 = QtWidgets.QLabel()
            label2.setFont(QFont("Roman times", 16))
            label2.setAlignment(qt.AlignCenter)
            label3 = QtWidgets.QLabel()
            widget = QtWidgets.QWidget()
            item = QListWidgetItem()

            if isinstance(path[i+1], list):
                if path[i+1][0]!="FILE":
                    item.setText(str(path[i+1][0]))
                    label.setText(str(path[i+1][0]))
                    label.setStyleSheet("background:rgb(220,130,80) ")
                else:
                    item.setText(str(path[i + 1][1]))
                    label.setText(str(path[i + 1][1]))
                    label.setStyleSheet("background:rgb(180,250,30) ")
                    long = 0
                    for m in path[i+1][2:]:
                        long += len(store[int(m)])
                    label2.setText("Size:"+str(long))

            label.setFixedSize(80,80)
            label2.setFixedSize(80, 80)
            layout.addWidget(label)
            layout.addWidget(label3)
            layout.addWidget(label2)
            widget.setLayout(layout)
            self.ui.widget.addItem(item)
            self.ui.widget.setItemWidget(item,widget)
        txt = "Home"
        temp = List
        for i in ppge:
            txt += "/"
            txt += temp[i][0]
            temp = temp[i]
        self.dirlabel.setText(txt)

    def GetPath(self):  # 获得当前位置
        temp = List  # 指针指向索引
        for i in range(len(ppge)):  # 根据当前位置索引在文建索引中前进
            temp = temp[ppge[i]]
        return temp

    def GotoDir(self,name):  # 当前位置索引更新函数
        if self.ui.widget.selectedItems():
            dellist = self.ui.widget.selectedItems()
            for delitem in dellist:
                del_item = self.ui.widget.takeItem(self.ui.widget.row(delitem))
                name = del_item.text()

            path = self.GetPath()
            for i in range(1, len(path)):
                if path[i].count(name):
                    if path[i][0]!="FILE":
                        ppge.append(i)
                        break
                    else:
                        self.txt = ""
                        for j in path[i][2:]:
                            for m in store[int(j)]:
                                self.txt += str(m)
                        self.textbox.setText(self.txt)
                        self.filepointer = i
                        self.FileWindow.setHidden(False)
            self.ShowDir()

    def CreateDir(self):  # 创建文件夹（在当前位置）
        self.InputName(0)

    def DeleteDir(self):  # 删除文件夹（按name）
        if self.ui.widget.selectedItems():
            dellist = self.ui.widget.selectedItems()
            for delitem in dellist:
                del_item = self.ui.widget.takeItem(self.ui.widget.row(delitem))

                name = del_item.text()
                del del_item
            path = self.GetPath()
            for i in range(1, len(path)):
                if path[i][0] == name:
                    for j in path[i][1:]:
                        self.deletedir(j)
                    del path[i]
                    break           #这里如果不break，当你删去一个时，list长度减一但是i不减，path[i]就会越界
                elif path[i][0] == "FILE":
                    if path[i][1] == name:
                        for m in path[i][2:]:
                            store[int(m)].clear()
                        del path[i]
                        break  # 这里如果不break，当你删去一个时，list长度减一但是i不减，path[i]就会越界

            self.ShowDir()
            self.Refresh()

    def deletedir(self,dir):
        if dir[0] == "FILE":
            for m in dir[2:]:
                store[int(m)].clear()
            del dir
        else:
            for i in dir[1:]:
                self.deletedir(i)

    def ShowDir(self):  # 显示文件表
        temp = List
        global dirlist
        dirlist = "Home\n"
        showdir(temp, 0)  # 递归
        self.ui.label_200.setText(dirlist)
        self.ShowFiles()

#文件部分

    def CreateFile(self):  # 创建文件
        self.InputName(1)

    def OpenFile(self,name):
        self.GetPath().index(name)
        pass;

    def Manager(self):
        for i in range(30):
            if len(store[i]):
                continue
            else:
                return i
        return -1

    def Store(self):  # 退出时保存到txt
        if os.path.exists("List.txt"):
            os.remove("List.txt")
        fd = open("List.txt", 'w')
        if os.path.exists("Store.txt"):
            os.remove("Store.txt")
        fe = open("Store.txt", 'w')
        for i in range(30):
            if len(store[i]):
                for j in range(len(store[i])):
                    print(store[i][j], file=fe, end=" ")
                print(' ', file=fe)

        self.storedir(List, 0, fd)

    def storedir(self,temp, m, fd):  # 递归保存文件列表
        for i in range(len(temp)):
            l = m
            if isinstance(temp[i], list):
                if temp[i][0] == "FILE":
                    print(l + 1, '-', temp[i][1], file=fd,end=" ")
                    for j in temp[i][2:]:
                        print(j, file=fd, end=" ")
                    print(' ',file=fd)
                else:
                    l += 1
                    print(l, '+', temp[i][0], file=fd)
                    self.storedir(temp[i], l, fd)


def showdir(temp, m):  # 递归显示文件
    global dirlist
    for i in range(len(temp)):
        l = m
        if isinstance(temp[i], list):
            if temp[i][0] == "FILE":
                for j in range(l + 1):
                    dirlist += "    "
                dirlist += temp[i][1]
                dirlist += '\n'
            else:
                l += 1
                for j in range(l):
                    dirlist += "    "
                dirlist += temp[i][0]
                dirlist += '+'
                dirlist += '\n'
                showdir(temp[i], l)


app = QtWidgets.QApplication([])
application = myWindow()
application.show()

sys.exit(app.exec())