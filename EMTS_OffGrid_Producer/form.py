###################################################################################
# -*- coding: utf-8 -*-                                                           #
#                                                                                 #
# Ce code est formé de 3 parties:                                                 #
#                                                                                 #
# 1- Initialisation : appel des methodes et initialisation des variables globales #
#                                                                                 #
# 2- les classes suivies de leurs methodes :                                      #
#                                                                                 #
#       classes MplCanvas et MplWidget pour la creation du graphique              #
#                                                                                 #
#       classe Ui_Dialog pour creation d'une boite de dialogue qui s'ouvre suite  #
#       à l'apuis sur une barre de la courbe.                                     #
#                                                                                 #
#       classe Ui_Form pour la creation de toute l'interface suivie des methodes  #
#       pour communiquer avec le Venus GX par SSH.                                #
#                                                                                 #
# 3- finalement le main pour executer le programme.                               #
#                                                                                 #
# NB : Tous les parties de codes entre """....""" sont reliées au SSH.            #
# login :''           voir la fonction : def loginbt_on_click():                  #
# mot de passe : ''                                                               #
#                                                                                 #
###################################################################################




from PyQt5 import QtCore, QtGui, QtWidgets
import paramiko
import time
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import requests
import pyqtgraph as pg
import numpy as np
import math
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.text import Text
import time

#----------------------------------------

global n
global index 
global bar_width
global opacity

n=25
index = np.arange(n)
bar_width = -0.3
opacity = 0.9

#----------------------------------------
#----------------------------------------

class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

#----------------------------------------
#----------------------------------------
        
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   
        self.canvas = MplCanvas()                  
        self.vbl = QtWidgets.QVBoxLayout()         
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

#----------------------------------------
#----------------------------------------

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 211)
        Dialog.setStyleSheet("background-color: rgb(46, 105, 164);")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(220, 130, 191, 31))
        self.pushButton.setStyleSheet("color: rgb(255, 255, 255);\n""font: 8pt \"Palatino Linotype\";")
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 10, 481, 81))
        self.label.setStyleSheet("font: 12pt \"Palatino Linotype\";\n""color: rgb(255, 255, 255);")
        self.label.setObjectName("label")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "go to energy exchange portal"))
        self.label.setText(_translate("Dialog", "you may have a surplus or lack of energy at this hour tomorrow "))
        
#----------------------------------------
        
def onpick1(event):
    # -- cette fonction se declanche lorsque l'utilisateur appuis sur un barre de la courbe
    # -- pour ouvrir une boite de dialogue (pour vendre le surplus d'energie)
    if isinstance(event.artist,Rectangle):
        patch = event.artist
        Dialog = QtWidgets.QDialog()
        ui = Ui_Dialog()
        ui.setupUi(Dialog)
        Dialog.show()         
        Dialog.exec_()
        
#----------------------------------------
#----------------------------------------

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1024, 600)
        Form.setMinimumSize(QtCore.QSize(1024, 600))
        Form.setMaximumSize(QtCore.QSize(1024, 600))
        # -------------------  connection SSH -----------
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.target_host = '192.168.43.45'
            self.target_port = 22
            self.pwd = '123456'
            self.un = 'root'
            self.ssh.connect( hostname = self.target_host , username = self.un, password = self.pwd )
            self.ssh.get_transport().window_size = 3 *1024 * 1024 
        except:
            QtWidgets.QMessageBox.warning(Form, 'Error', 'No connection could be established, check that the Wifi Access Point is activated and try again ...')
        # ----------------------------------------------
       
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/sofrecomlogo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        Form.setStyleSheet("background-color: rgb(46, 105, 164);")
        self.MainStackWidget = QtWidgets.QStackedWidget(Form)
        self.MainStackWidget.setGeometry(QtCore.QRect(0, 0, 1024, 600))
        self.MainStackWidget.setMinimumSize(QtCore.QSize(1024, 600))
        self.MainStackWidget.setMaximumSize(QtCore.QSize(1024, 600))
        self.MainStackWidget.setStyleSheet("background-color: rgb(46, 105, 164);")
        self.MainStackWidget.setObjectName("MainStackWidget")
        self.page_0 = QtWidgets.QWidget()
        self.page_0.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.page_0.setObjectName("page_0")
        self.login = QtWidgets.QLineEdit(self.page_0)
        self.login.setGeometry(QtCore.QRect(200, 400, 250, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.login.setFont(font)
        self.login.setStyleSheet("border-radius: 15px;\n"
"border: 2px solid gray;\n"
"background-color: rgb(226, 226, 226);")
        self.login.setObjectName("login")
        self.loginbt = QtWidgets.QPushButton(self.page_0)
        self.loginbt.setGeometry(QtCore.QRect(650, 500, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(22)
        self.loginbt.setFont(font)
        self.loginbt.setStyleSheet("background-color: rgb(56, 125, 197);\n"
"border-radius: 20px;\n"
"color: rgb(255, 255, 255);")
        self.loginbt.setObjectName("loginbt")
        self.label_10 = QtWidgets.QLabel(self.page_0)
        self.label_10.setGeometry(QtCore.QRect(510, 400, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(22)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_12 = QtWidgets.QLabel(self.page_0)
        self.label_12.setGeometry(QtCore.QRect(212, 250, 600, 100))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(48)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.label = QtWidgets.QLabel(self.page_0)
        self.label.setGeometry(QtCore.QRect(50, 400, 100, 50))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(24)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.password = QtWidgets.QLineEdit(self.page_0)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password) #--- password *****
        self.password.setGeometry(QtCore.QRect(710, 400, 250, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.password.setFont(font)
        self.password.setStyleSheet("border-radius: 15px;\n"
"border: 2px solid gray;\n"
"background-color: rgb(226, 226, 226);")
        self.password.setObjectName("password")
        self.label_18 = QtWidgets.QLabel(self.page_0)
        self.label_18.setGeometry(QtCore.QRect(730, 40, 250, 150))
        self.label_18.setText("")
        self.label_18.setPixmap(QtGui.QPixmap("images/sofrecomlogo.png"))
        self.label_18.setScaledContents(True)
        self.label_18.setObjectName("label_18")
        self.label_13 = QtWidgets.QLabel(self.page_0)
        self.label_13.setGeometry(QtCore.QRect(50, 40, 250, 150))
        self.label_13.setText("")
        self.label_13.setPixmap(QtGui.QPixmap("images/centrelogo.jpg"))
        self.label_13.setScaledContents(True)
        self.label_13.setObjectName("label_13")
        self.exitAppbtn = QtWidgets.QPushButton(self.page_0)
        self.exitAppbtn.setGeometry(QtCore.QRect(850, 500, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(22)
        self.exitAppbtn.setFont(font)
        self.exitAppbtn.setStyleSheet("background-color: rgb(56, 125, 197);\n"
"border-radius: 20px;\n"
"color: rgb(255, 255, 255);")
        self.exitAppbtn.setObjectName("exitAppbtn")
        self.MainStackWidget.addWidget(self.page_0)
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.SolarPanel = QtWidgets.QWidget(self.page_1)
        self.SolarPanel.setGeometry(QtCore.QRect(30, 30, 305, 255))
        self.SolarPanel.setStyleSheet("background-color: rgb(56, 125, 197);border-radius: 30px;")
        self.SolarPanel.setObjectName("SolarPanel")
        self.solarIMG = QtWidgets.QLabel(self.SolarPanel)
        self.solarIMG.setGeometry(QtCore.QRect(175, 15, 100, 80))
        self.solarIMG.setText("")
        self.solarIMG.setPixmap(QtGui.QPixmap("images/solar.png"))
        self.solarIMG.setScaledContents(True)
        self.solarIMG.setObjectName("solarIMG")
        self.label_2 = QtWidgets.QLabel(self.SolarPanel)
        self.label_2.setGeometry(QtCore.QRect(0, 110, 305, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background-color: rgb(76, 138, 203);\n"
"color: rgb(201, 220, 239);")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.SolarPanel)
        self.label_3.setGeometry(QtCore.QRect(20, 140, 25, 25))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("images/voltage.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.SolarPanel)
        self.label_4.setGeometry(QtCore.QRect(50, 140, 53, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.SolarPanel)
        self.label_5.setGeometry(QtCore.QRect(20, 180, 25, 25))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("images/current.png"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.SolarPanel)
        self.label_6.setGeometry(QtCore.QRect(50, 180, 51, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_6.setObjectName("label_6")
        self.spA = QtWidgets.QLCDNumber(self.SolarPanel)
        self.spA.setGeometry(QtCore.QRect(160, 180, 90, 25))
        self.spA.setStyleSheet("color: rgb(255, 255, 255);")
        self.spA.setDigitCount(7)
        self.spA.setProperty("value", 0)
        self.spA.setObjectName("spA")
        self.spV = QtWidgets.QLCDNumber(self.SolarPanel)
        self.spV.setGeometry(QtCore.QRect(160, 140, 90, 25))
        self.spV.setStyleSheet("color: rgb(255, 255, 255);")
        self.spV.setDigitCount(7)
        self.spV.setProperty("value", 0)
        self.spV.setObjectName("spV")
        self.label_37 = QtWidgets.QLabel(self.SolarPanel)
        self.label_37.setGeometry(QtCore.QRect(268, 180, 13, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_37.setFont(font)
        self.label_37.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_37.setObjectName("label_37")
        self.label_34 = QtWidgets.QLabel(self.SolarPanel)
        self.label_34.setGeometry(QtCore.QRect(268, 140, 13, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_34.setFont(font)
        self.label_34.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_34.setObjectName("label_34")
        self.label_7 = QtWidgets.QLabel(self.SolarPanel)
        self.label_7.setGeometry(QtCore.QRect(40, 10, 53, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.SolarPanel)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.label_8.setText("")
        self.label_8.setPixmap(QtGui.QPixmap("images/power.png"))
        self.label_8.setScaledContents(True)
        self.label_8.setObjectName("label_8")
        self.label_36 = QtWidgets.QLabel(self.SolarPanel)
        self.label_36.setGeometry(QtCore.QRect(165, 80, 20, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_36.setFont(font)
        self.label_36.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_36.setObjectName("label_36")
        self.spW = QtWidgets.QLCDNumber(self.SolarPanel)
        self.spW.setGeometry(QtCore.QRect(0, 40, 161, 51))
        self.spW.setStyleSheet("color: rgb(255, 255, 255);")
        self.spW.setDigitCount(6)
        self.spW.setProperty("value", 0)
        self.spW.setObjectName("spW")
        self.Battery = QtWidgets.QWidget(self.page_1)
        self.Battery.setGeometry(QtCore.QRect(30, 315, 305, 255))
        self.Battery.setStyleSheet("background-color: rgb(56, 125, 197);border-radius: 30px;")
        self.Battery.setObjectName("Battery")
        self.label_27 = QtWidgets.QLabel(self.Battery)
        self.label_27.setGeometry(QtCore.QRect(0, 110, 305, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_27.setFont(font)
        self.label_27.setStyleSheet("background-color: rgb(76, 138, 203);\n"
"color: rgb(201, 220, 239);")
        self.label_27.setObjectName("label_27")
        self.batIMG = QtWidgets.QLabel(self.Battery)
        self.batIMG.setGeometry(QtCore.QRect(175, 15, 100, 80))
        self.batIMG.setText("")
        self.batIMG.setPixmap(QtGui.QPixmap("images/battery.png"))
        self.batIMG.setScaledContents(True)
        self.batIMG.setObjectName("batIMG")
        self.BatterystackedWidget = QtWidgets.QStackedWidget(self.Battery)
        self.BatterystackedWidget.setGeometry(QtCore.QRect(8, 133, 290, 120))
        self.BatterystackedWidget.setStyleSheet("background-color: rgb(56, 125, 197);\n"
"border-radius: 15px;")
        self.BatterystackedWidget.setObjectName("BatterystackedWidget")
        self.pageB1 = QtWidgets.QWidget()
        self.pageB1.setStyleSheet("background-color: rgb(56, 125, 197);")
        self.pageB1.setObjectName("pageB1")
        self.label_39 = QtWidgets.QLabel(self.pageB1)
        self.label_39.setGeometry(QtCore.QRect(260, 90, 13, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_39.setFont(font)
        self.label_39.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_39.setObjectName("label_39")
        self.label_41 = QtWidgets.QLabel(self.pageB1)
        self.label_41.setGeometry(QtCore.QRect(260, 10, 20, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_41.setFont(font)
        self.label_41.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_41.setObjectName("label_41")
        self.label_31 = QtWidgets.QLabel(self.pageB1)
        self.label_31.setGeometry(QtCore.QRect(12, 90, 25, 25))
        self.label_31.setText("")
        self.label_31.setPixmap(QtGui.QPixmap("images/current battery.png"))
        self.label_31.setScaledContents(True)
        self.label_31.setObjectName("label_31")
        self.batV = QtWidgets.QLCDNumber(self.pageB1)
        self.batV.setGeometry(QtCore.QRect(152, 50, 90, 25))
        self.batV.setStyleSheet("color: rgb(255, 255, 255);")
        self.batV.setDigitCount(7)
        self.batV.setProperty("value", 0)
        self.batV.setObjectName("batV")
        self.label_25 = QtWidgets.QLabel(self.pageB1)
        self.label_25.setGeometry(QtCore.QRect(42, 90, 51, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_25.setFont(font)
        self.label_25.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_25.setObjectName("label_25")
        self.label_28 = QtWidgets.QLabel(self.pageB1)
        self.label_28.setGeometry(QtCore.QRect(42, 10, 53, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_28.setFont(font)
        self.label_28.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_28.setObjectName("label_28")
        self.label_30 = QtWidgets.QLabel(self.pageB1)
        self.label_30.setGeometry(QtCore.QRect(12, 10, 25, 25))
        self.label_30.setText("")
        self.label_30.setPixmap(QtGui.QPixmap("images/power battery.png"))
        self.label_30.setScaledContents(True)
        self.label_30.setObjectName("label_30")
        self.batW = QtWidgets.QLCDNumber(self.pageB1)
        self.batW.setGeometry(QtCore.QRect(152, 10, 90, 25))
        self.batW.setStyleSheet("color: rgb(255, 255, 255);")
        self.batW.setDigitCount(7)
        self.batW.setProperty("value", 0)
        self.batW.setObjectName("batW")
        self.label_40 = QtWidgets.QLabel(self.pageB1)
        self.label_40.setGeometry(QtCore.QRect(260, 50, 13, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_40.setFont(font)
        self.label_40.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_40.setObjectName("label_40")
        self.label_29 = QtWidgets.QLabel(self.pageB1)
        self.label_29.setGeometry(QtCore.QRect(12, 50, 25, 25))
        self.label_29.setText("")
        self.label_29.setPixmap(QtGui.QPixmap("images/voltage battery.png"))
        self.label_29.setScaledContents(True)
        self.label_29.setObjectName("label_29")
        self.label_26 = QtWidgets.QLabel(self.pageB1)
        self.label_26.setGeometry(QtCore.QRect(42, 50, 53, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_26.setFont(font)
        self.label_26.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_26.setObjectName("label_26")
        self.batA = QtWidgets.QLCDNumber(self.pageB1)
        self.batA.setGeometry(QtCore.QRect(152, 90, 90, 25))
        self.batA.setStyleSheet("color: rgb(255, 255, 255);")
        self.batA.setDigitCount(7)
        self.batA.setProperty("value", 0)
        self.batA.setObjectName("batA")
        self.BatterystackedWidget.addWidget(self.pageB1)
        self.pageB2 = QtWidgets.QWidget()
        self.pageB2.setStyleSheet("background-color: rgb(56, 125, 197);")
        self.pageB2.setObjectName("pageB2")
        self.label_66 = QtWidgets.QLabel(self.pageB2)
        self.label_66.setGeometry(QtCore.QRect(10, 50, 25, 25))
        self.label_66.setText("")
        self.label_66.setPixmap(QtGui.QPixmap("images/ralaybattery.png"))
        self.label_66.setScaledContents(True)
        self.label_66.setObjectName("label_66")
        self.batAh = QtWidgets.QLCDNumber(self.pageB2)
        self.batAh.setGeometry(QtCore.QRect(150, 10, 90, 25))
        self.batAh.setStyleSheet("color: rgb(255, 255, 255);")
        self.batAh.setDigitCount(7)
        self.batAh.setProperty("value", 0)
        self.batAh.setObjectName("batAh")
        self.label_68 = QtWidgets.QLabel(self.pageB2)
        self.label_68.setGeometry(QtCore.QRect(40, 50, 121, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_68.setFont(font)
        self.label_68.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_68.setObjectName("label_68")
        self.label_71 = QtWidgets.QLabel(self.pageB2)
        self.label_71.setGeometry(QtCore.QRect(258, 10, 25, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_71.setFont(font)
        self.label_71.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_71.setObjectName("label_71")
        self.label_72 = QtWidgets.QLabel(self.pageB2)
        self.label_72.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.label_72.setText("")
        self.label_72.setPixmap(QtGui.QPixmap("images/consumedAh.png"))
        self.label_72.setScaledContents(True)
        self.label_72.setObjectName("label_72")
        self.label_73 = QtWidgets.QLabel(self.pageB2)
        self.label_73.setGeometry(QtCore.QRect(40, 10, 101, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_73.setFont(font)
        self.label_73.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_73.setObjectName("label_73")
        self.batRelay = QtWidgets.QLabel(self.pageB2)
        self.batRelay.setGeometry(QtCore.QRect(199, 50, 80, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.batRelay.setFont(font)
        self.batRelay.setStyleSheet("color: rgb(255, 255, 255);")
        self.batRelay.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.batRelay.setObjectName("batRelay")
        self.BatterystackedWidget.addWidget(self.pageB2)
        self.batterynextbtn = QtWidgets.QPushButton(self.Battery)
        self.batterynextbtn.setGeometry(QtCore.QRect(270, 110, 20, 20))
        self.batterynextbtn.setStyleSheet("background-color: rgb(76, 138, 203);")
        self.batterynextbtn.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.batterynextbtn.setIcon(icon1)
        self.batterynextbtn.setIconSize(QtCore.QSize(20, 20))
        self.batterynextbtn.setObjectName("batterynextbtn")
        self.batterybackbtn = QtWidgets.QPushButton(self.Battery)
        self.batterybackbtn.setGeometry(QtCore.QRect(250, 110, 20, 20))
        self.batterybackbtn.setStyleSheet("background-color: rgb(76, 138, 203);")
        self.batterybackbtn.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.batterybackbtn.setIcon(icon2)
        self.batterybackbtn.setIconSize(QtCore.QSize(20, 20))
        self.batterybackbtn.setObjectName("batterybackbtn")
        self.label_70 = QtWidgets.QLabel(self.Battery)
        self.label_70.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.label_70.setText("")
        self.label_70.setPixmap(QtGui.QPixmap("images/soc.png"))
        self.label_70.setScaledContents(True)
        self.label_70.setObjectName("label_70")
        self.label_69 = QtWidgets.QLabel(self.Battery)
        self.label_69.setGeometry(QtCore.QRect(40, 10, 111, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_69.setFont(font)
        self.label_69.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_69.setObjectName("label_69")
        self.label_65 = QtWidgets.QLabel(self.Battery)
        self.label_65.setGeometry(QtCore.QRect(143, 80, 30, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_65.setFont(font)
        self.label_65.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_65.setObjectName("label_65")
        self.soc = QtWidgets.QLCDNumber(self.Battery)
        self.soc.setGeometry(QtCore.QRect(15, 40, 120, 60))
        self.soc.setStyleSheet("color: rgb(255, 255, 255);")
        self.soc.setDigitCount(4)
        self.soc.setProperty("value", 0)
        self.soc.setObjectName("soc")
        self.Grid = QtWidgets.QWidget(self.page_1)
        self.Grid.setGeometry(QtCore.QRect(365, 30, 305, 255))
        self.Grid.setStyleSheet("background-color: rgb(56, 125, 197);border-radius: 30px;")
        self.Grid.setObjectName("Grid")
        self.gridIMG = QtWidgets.QLabel(self.Grid)
        self.gridIMG.setGeometry(QtCore.QRect(177, 15, 100, 80))
        self.gridIMG.setText("")
        self.gridIMG.setPixmap(QtGui.QPixmap("images/feed-in energy.png"))
        self.gridIMG.setScaledContents(True)
        self.gridIMG.setObjectName("gridIMG")
        self.label_67 = QtWidgets.QLabel(self.Grid)
        self.label_67.setGeometry(QtCore.QRect(50, 180, 51, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_67.setFont(font)
        self.label_67.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_67.setObjectName("label_67")
        self.label_74 = QtWidgets.QLabel(self.Grid)
        self.label_74.setGeometry(QtCore.QRect(50, 140, 53, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_74.setFont(font)
        self.label_74.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_74.setObjectName("label_74")
        self.gridA = QtWidgets.QLCDNumber(self.Grid)
        self.gridA.setGeometry(QtCore.QRect(160, 180, 90, 25))
        self.gridA.setStyleSheet("color: rgb(255, 255, 255);")
        self.gridA.setDigitCount(7)
        self.gridA.setProperty("value", 0)
        self.gridA.setObjectName("gridA")
        self.gridV = QtWidgets.QLCDNumber(self.Grid)
        self.gridV.setGeometry(QtCore.QRect(160, 140, 90, 25))
        self.gridV.setStyleSheet("color: rgb(255, 255, 255);")
        self.gridV.setDigitCount(7)
        self.gridV.setProperty("value", 0)
        self.gridV.setObjectName("gridV")
        self.gridW = QtWidgets.QLCDNumber(self.Grid)
        self.gridW.setGeometry(QtCore.QRect(0, 40, 161, 51))
        self.gridW.setStyleSheet("color: rgb(255, 255, 255);")
        self.gridW.setDigitCount(6)
        self.gridW.setProperty("value", 0)
        self.gridW.setObjectName("gridW")
        self.label_75 = QtWidgets.QLabel(self.Grid)
        self.label_75.setGeometry(QtCore.QRect(0, 110, 305, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_75.setFont(font)
        self.label_75.setStyleSheet("background-color: rgb(76, 138, 203);color: rgb(201, 220, 239);")
        self.label_75.setObjectName("label_75")
        self.label_77 = QtWidgets.QLabel(self.Grid)
        self.label_77.setGeometry(QtCore.QRect(268, 180, 13, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_77.setFont(font)
        self.label_77.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_77.setObjectName("label_77")
        self.label_78 = QtWidgets.QLabel(self.Grid)
        self.label_78.setGeometry(QtCore.QRect(20, 140, 25, 25))
        self.label_78.setText("")
        self.label_78.setPixmap(QtGui.QPixmap("images/voltage.png"))
        self.label_78.setScaledContents(True)
        self.label_78.setObjectName("label_78")
        self.label_80 = QtWidgets.QLabel(self.Grid)
        self.label_80.setGeometry(QtCore.QRect(20, 180, 25, 25))
        self.label_80.setText("")
        self.label_80.setPixmap(QtGui.QPixmap("images/current.png"))
        self.label_80.setScaledContents(True)
        self.label_80.setObjectName("label_80")
        self.label_81 = QtWidgets.QLabel(self.Grid)
        self.label_81.setGeometry(QtCore.QRect(165, 80, 20, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_81.setFont(font)
        self.label_81.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_81.setObjectName("label_81")
        self.label_82 = QtWidgets.QLabel(self.Grid)
        self.label_82.setGeometry(QtCore.QRect(268, 140, 13, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_82.setFont(font)
        self.label_82.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_82.setObjectName("label_82")
        self.label_79 = QtWidgets.QLabel(self.Grid)
        self.label_79.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.label_79.setText("")
        self.label_79.setPixmap(QtGui.QPixmap("images/power.png"))
        self.label_79.setScaledContents(True)
        self.label_79.setObjectName("label_79")
        self.label_76 = QtWidgets.QLabel(self.Grid)
        self.label_76.setGeometry(QtCore.QRect(40, 10, 53, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_76.setFont(font)
        self.label_76.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_76.setObjectName("label_76")
        self.Home = QtWidgets.QWidget(self.page_1)
        self.Home.setGeometry(QtCore.QRect(365, 315, 305, 255))
        self.Home.setStyleSheet("background-color: rgb(56, 125, 197);border-radius: 30px;")
        self.Home.setObjectName("Home")
        self.label_92 = QtWidgets.QLabel(self.Home)
        self.label_92.setGeometry(QtCore.QRect(165, 80, 20, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_92.setFont(font)
        self.label_92.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_92.setObjectName("label_92")
        self.label_89 = QtWidgets.QLabel(self.Home)
        self.label_89.setGeometry(QtCore.QRect(268, 180, 13, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_89.setFont(font)
        self.label_89.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_89.setObjectName("label_89")
        self.label_84 = QtWidgets.QLabel(self.Home)
        self.label_84.setGeometry(QtCore.QRect(50, 180, 51, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_84.setFont(font)
        self.label_84.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_84.setObjectName("label_84")
        self.label_86 = QtWidgets.QLabel(self.Home)
        self.label_86.setGeometry(QtCore.QRect(0, 110, 305, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_86.setFont(font)
        self.label_86.setStyleSheet("background-color: rgb(76, 138, 203);\n"
"color: rgb(201, 220, 239);")
        self.label_86.setObjectName("label_86")
        self.label_87 = QtWidgets.QLabel(self.Home)
        self.label_87.setGeometry(QtCore.QRect(10, 10, 25, 25))
        self.label_87.setText("")
        self.label_87.setPixmap(QtGui.QPixmap("images/power.png"))
        self.label_87.setScaledContents(True)
        self.label_87.setObjectName("label_87")
        self.label_91 = QtWidgets.QLabel(self.Home)
        self.label_91.setGeometry(QtCore.QRect(20, 140, 25, 25))
        self.label_91.setText("")
        self.label_91.setPixmap(QtGui.QPixmap("images/voltage.png"))
        self.label_91.setScaledContents(True)
        self.label_91.setObjectName("label_91")
        self.houseIMG = QtWidgets.QLabel(self.Home)
        self.houseIMG.setGeometry(QtCore.QRect(177, 15, 100, 80))
        self.houseIMG.setText("")
        self.houseIMG.setPixmap(QtGui.QPixmap("images/house.png"))
        self.houseIMG.setScaledContents(True)
        self.houseIMG.setObjectName("houseIMG")
        self.homeV = QtWidgets.QLCDNumber(self.Home)
        self.homeV.setGeometry(QtCore.QRect(160, 140, 90, 25))
        self.homeV.setStyleSheet("color: rgb(255, 255, 255);")
        self.homeV.setDigitCount(7)
        self.homeV.setProperty("value", 0)
        self.homeV.setObjectName("homeV")
        self.label_90 = QtWidgets.QLabel(self.Home)
        self.label_90.setGeometry(QtCore.QRect(268, 140, 13, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_90.setFont(font)
        self.label_90.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_90.setObjectName("label_90")
        self.homeA = QtWidgets.QLCDNumber(self.Home)
        self.homeA.setGeometry(QtCore.QRect(160, 180, 90, 25))
        self.homeA.setStyleSheet("color: rgb(255, 255, 255);")
        self.homeA.setDigitCount(7)
        self.homeA.setProperty("value", 0)
        self.homeA.setObjectName("homeA")
        self.label_83 = QtWidgets.QLabel(self.Home)
        self.label_83.setGeometry(QtCore.QRect(20, 180, 25, 25))
        self.label_83.setText("")
        self.label_83.setPixmap(QtGui.QPixmap("images/current.png"))
        self.label_83.setScaledContents(True)
        self.label_83.setObjectName("label_83")
        self.label_85 = QtWidgets.QLabel(self.Home)
        self.label_85.setGeometry(QtCore.QRect(40, 10, 53, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_85.setFont(font)
        self.label_85.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_85.setObjectName("label_85")
        self.label_88 = QtWidgets.QLabel(self.Home)
        self.label_88.setGeometry(QtCore.QRect(50, 140, 53, 25))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label_88.setFont(font)
        self.label_88.setStyleSheet("color: rgb(201, 220, 239);")
        self.label_88.setObjectName("label_88")
        self.homeW = QtWidgets.QLCDNumber(self.Home)
        self.homeW.setGeometry(QtCore.QRect(0, 40, 161, 51))
        self.homeW.setStyleSheet("color: rgb(255, 255, 255);")
        self.homeW.setDigitCount(6)
        self.homeW.setProperty("value", 0)
        self.homeW.setObjectName("homeW")
        self.line = QtWidgets.QFrame(self.page_1)
        self.line.setGeometry(QtCore.QRect(700, 0, 10, 600))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.weather = QtWidgets.QWidget(self.page_1)
        self.weather.setGeometry(QtCore.QRect(740, 100, 250, 470))
        self.weather.setStyleSheet("background-color: rgb(56, 125, 197);border-radius: 30px;")
        self.weather.setObjectName("weather")
        self.WeatherImage = QtWidgets.QLabel(self.weather)
        self.WeatherImage.setGeometry(QtCore.QRect(0, 75, 71, 71))
        self.WeatherImage.setText("")
        self.WeatherImage.setPixmap(QtGui.QPixmap("images/01d.png"))
        self.WeatherImage.setScaledContents(True)
        self.WeatherImage.setObjectName("WeatherImage")
        self.label_106 = QtWidgets.QLabel(self.weather)
        self.label_106.setGeometry(QtCore.QRect(180, 71, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_106.setFont(font)
        self.label_106.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_106.setObjectName("label_106")
        self.Temp = QtWidgets.QLCDNumber(self.weather)
        self.Temp.setGeometry(QtCore.QRect(75, 65, 100, 90))
        self.Temp.setDigitCount(2)
        self.Temp.setProperty("value", 0)
        self.Temp.setObjectName("Temp")
        self.Localisation = QtWidgets.QLabel(self.weather)
        self.Localisation.setGeometry(QtCore.QRect(0, 25, 250, 30))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.Localisation.setFont(font)
        self.Localisation.setStyleSheet("color: rgb(255, 255, 255);")
        self.Localisation.setAlignment(QtCore.Qt.AlignCenter)
        self.Localisation.setObjectName("Localisation")
        self.description = QtWidgets.QLabel(self.weather)
        self.description.setGeometry(QtCore.QRect(0, 180, 250, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.description.setFont(font)
        self.description.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(76, 138, 203);")
        self.description.setAlignment(QtCore.Qt.AlignCenter)
        self.description.setObjectName("description")
        self.TmaxTmin = QtWidgets.QLabel(self.weather)
        self.TmaxTmin.setGeometry(QtCore.QRect(0, 160, 250, 15))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.TmaxTmin.setFont(font)
        self.TmaxTmin.setStyleSheet("color: rgb(255, 255, 255);")
        self.TmaxTmin.setAlignment(QtCore.Qt.AlignCenter)
        self.TmaxTmin.setObjectName("TmaxTmin")
        self.pressure = QtWidgets.QLabel(self.weather)
        self.pressure.setGeometry(QtCore.QRect(0, 210, 250, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pressure.setFont(font)
        self.pressure.setStyleSheet("color: rgb(255, 255, 255);")
        self.pressure.setAlignment(QtCore.Qt.AlignCenter)
        self.pressure.setObjectName("pressure")
        self.humidity = QtWidgets.QLabel(self.weather)
        self.humidity.setGeometry(QtCore.QRect(0, 230, 250, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.humidity.setFont(font)
        self.humidity.setStyleSheet("color: rgb(255, 255, 255);")
        self.humidity.setAlignment(QtCore.Qt.AlignCenter)
        self.humidity.setObjectName("humidity")
        self.visibility = QtWidgets.QLabel(self.weather)
        self.visibility.setGeometry(QtCore.QRect(0, 250, 250, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.visibility.setFont(font)
        self.visibility.setStyleSheet("color: rgb(255, 255, 255);")
        self.visibility.setAlignment(QtCore.Qt.AlignCenter)
        self.visibility.setObjectName("visibility")
        self.windspeed = QtWidgets.QLabel(self.weather)
        self.windspeed.setGeometry(QtCore.QRect(0, 270, 250, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.windspeed.setFont(font)
        self.windspeed.setStyleSheet("color: rgb(255, 255, 255);")
        self.windspeed.setAlignment(QtCore.Qt.AlignCenter)
        self.windspeed.setObjectName("windspeed")
        self.sunrise = QtWidgets.QLabel(self.weather)
        self.sunrise.setGeometry(QtCore.QRect(0, 290, 250, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.sunrise.setFont(font)
        self.sunrise.setStyleSheet("color: rgb(255, 255, 255);")
        self.sunrise.setAlignment(QtCore.Qt.AlignCenter)
        self.sunrise.setObjectName("sunrise")
        self.sunset = QtWidgets.QLabel(self.weather)
        self.sunset.setGeometry(QtCore.QRect(0, 310, 250, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.sunset.setFont(font)
        self.sunset.setStyleSheet("color: rgb(255, 255, 255);")
        self.sunset.setAlignment(QtCore.Qt.AlignCenter)
        self.sunset.setObjectName("sunset")
        self.Relay1 = QtWidgets.QPushButton(self.weather)
        self.Relay1.setGeometry(QtCore.QRect(70, 410, 50, 50))
        self.Relay1.setText("")
        self.Relay1.setIcon(QtGui.QIcon(QtGui.QPixmap("images/on.png"))) # ----- icon
        self.Relay1.setIconSize(QtCore.QSize(50, 50))
        self.Relay1.setObjectName("Relay1")
        self.label_105 = QtWidgets.QLabel(self.weather)
        self.label_105.setGeometry(QtCore.QRect(0, 370, 250, 30))
        font = QtGui.QFont()
        font.setFamily("Arial Rounded MT Bold")
        font.setPointSize(20)
        font.setBold(False)
        font.setWeight(50)
        self.label_105.setFont(font)
        self.label_105.setStyleSheet("color: rgb(255, 255, 255);background-color: rgb(76, 138, 203);")
        self.label_105.setAlignment(QtCore.Qt.AlignCenter)
        self.label_105.setObjectName("label_105")
        self.Relay2 = QtWidgets.QPushButton(self.weather)
        self.Relay2.setGeometry(QtCore.QRect(130, 410, 50, 50))
        self.Relay2.setText("")
        self.Relay2.setIcon(QtGui.QIcon(QtGui.QPixmap("images/on.png"))) # ----- icon
        self.Relay2.setIconSize(QtCore.QSize(50, 50))
        self.Relay2.setObjectName("Relay2")
        self.backbtn = QtWidgets.QPushButton(self.page_1)
        self.backbtn.setGeometry(QtCore.QRect(740, 30, 100, 50))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(22)
        self.backbtn.setFont(font)
        self.backbtn.setStyleSheet("background-color: rgb(56, 125, 197);\n"
"border-radius: 20px;\n"
"color: rgb(255, 255, 255);")
        self.backbtn.setObjectName("backbtn")
        self.graphbtn = QtWidgets.QPushButton(self.page_1)
        self.graphbtn.setGeometry(QtCore.QRect(890, 30, 100, 50))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(22)
        self.graphbtn.setFont(font)
        self.graphbtn.setStyleSheet("background-color: rgb(56, 125, 197);\n"
"border-radius: 20px;\n"
"color: rgb(255, 255, 255);")
        self.graphbtn.setObjectName("graphbtn")
        self.MainStackWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.back2btn = QtWidgets.QPushButton(self.page_2)
        self.back2btn.setGeometry(QtCore.QRect(740, 30, 100, 50))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(22)
        self.back2btn.setFont(font)
        self.back2btn.setStyleSheet("background-color: rgb(56, 125, 197);\n"
"border-radius: 20px;\n"
"color: rgb(255, 255, 255);")
        self.back2btn.setObjectName("back2btn")
        self.exitbt = QtWidgets.QPushButton(self.page_2)
        self.exitbt.setGeometry(QtCore.QRect(890, 30, 100, 50))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(22)
        self.exitbt.setFont(font)
        self.exitbt.setStyleSheet("background-color: rgb(56, 125, 197);\n"
"border-radius: 20px;\n"
"color: rgb(255, 255, 255);")
        self.exitbt.setObjectName("exitbt")
        self.graphwidget = MplWidget(self.page_2)
        self.graphwidget.setGeometry(QtCore.QRect(30, 90, 960, 500)) # apres modif
        self.graphwidget.setObjectName("graphwidget")
        self.MainStackWidget.addWidget(self.page_2)
        
        
        # --------------- __init__ --------------
        
        self.retranslateUi(Form)
        self.MainStackWidget.setCurrentIndex(0)
        self.BatterystackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

        # ----------------- Button actions ------
        
        self.graphbtn.clicked.connect(self.update_all) #--- click
        self.loginbt.clicked.connect(self.loginbt_on_click) #--- click
        self.exitAppbtn.clicked.connect(self.exitAppbtn_on_click) #--- click
        self.batterynextbtn.clicked.connect(self.batterynextbtn_on_click) #--- click
        self.batterybackbtn.clicked.connect(self.batterybackbtn_on_click) #--- click
        self.backbtn.clicked.connect(self.backbtn_on_click) #--- click
        self.exitbt.clicked.connect(self.backbtn_on_click) #---- click
        self.back2btn.clicked.connect(self.overviewbt_on_click) #--- click	
        self.Relay1.clicked.connect(self.relay1_on_click) #--- click	
        self.Relay2.clicked.connect(self.relay2_on_click) #--- click

        #----------------------------------------

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "IHM"))
        self.loginbt.setText(_translate("Form", "Login"))
        self.label_10.setText(_translate("Form", "Password"))
        self.label_12.setText(_translate("Form", "Home Energy Monitor"))
        self.label.setText(_translate("Form", "Login"))
        self.exitAppbtn.setText(_translate("Form", "Exit"))
        self.label_2.setText(_translate("Form", "  Solar Panel"))
        self.label_4.setText(_translate("Form", "Voltage"))
        self.label_6.setText(_translate("Form", "Current"))
        self.label_37.setText(_translate("Form", "A"))
        self.label_34.setText(_translate("Form", "V"))
        self.label_7.setText(_translate("Form", "Power"))
        self.label_36.setText(_translate("Form", "W"))
        self.label_27.setText(_translate("Form", "  Battery"))
        self.label_39.setText(_translate("Form", "A"))
        self.label_41.setText(_translate("Form", "W"))
        self.label_25.setText(_translate("Form", "Current"))
        self.label_28.setText(_translate("Form", "Power"))
        self.label_40.setText(_translate("Form", "V"))
        self.label_26.setText(_translate("Form", "Voltage"))
        self.label_68.setText(_translate("Form", "State of Relay"))
        self.label_71.setText(_translate("Form", "Ah"))
        self.label_73.setText(_translate("Form", "Consumed Ah"))
        self.batRelay.setText(_translate("Form", "--"))
        self.label_69.setText(_translate("Form", "State of charge"))
        self.label_65.setText(_translate("Form", "%"))
        self.label_67.setText(_translate("Form", "Current"))
        self.label_74.setText(_translate("Form", "Voltage"))
        self.label_75.setText(_translate("Form", "  Fed into the Grid"))
        self.label_77.setText(_translate("Form", "A"))
        self.label_81.setText(_translate("Form", "W"))
        self.label_82.setText(_translate("Form", "V"))
        self.label_76.setText(_translate("Form", "Power"))
        self.label_92.setText(_translate("Form", "W"))
        self.label_89.setText(_translate("Form", "A"))
        self.label_84.setText(_translate("Form", "Current"))
        self.label_86.setText(_translate("Form", "  Consumption"))
        self.label_90.setText(_translate("Form", "V"))
        self.label_85.setText(_translate("Form", "Power"))
        self.label_88.setText(_translate("Form", "Voltage"))
        self.label_106.setText(_translate("Form", "°C"))
        self.Localisation.setText(_translate("Form", "Tunis"))
        self.description.setText(_translate("Form", "Clear sky"))
        self.TmaxTmin.setText(_translate("Form", " T min : -- °C    T max : -- °C"))
        self.pressure.setText(_translate("Form", "Pressure : ---- hPa"))
        self.humidity.setText(_translate("Form", "Humidity : -- %"))
        self.visibility.setText(_translate("Form", "Visibility : -- km"))
        self.windspeed.setText(_translate("Form", "Wind : -- km/h"))
        self.sunrise.setText(_translate("Form", "Sunrise : --:--:--"))
        self.sunset.setText(_translate("Form", "Sunset : --:--:-- "))
        self.label_105.setText(_translate("Form", "Household Load"))
        self.backbtn.setText(_translate("Form", "Back"))
        self.graphbtn.setText(_translate("Form", "Refresh "))
        self.back2btn.setText(_translate("Form", "Back"))
        self.exitbt.setText(_translate("Form", "Exit"))
        
    #----------------------------------------
        
    def weather_data(self):
        # -- fonction pour afficher les données météorologiques pour une ville : "Tunis" dans notre cas
        _translate = QtCore.QCoreApplication.translate
        try :
            api_address="http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
            city="tunis"   # a changer 
            url = api_address + city
            data = requests.get(url).json()
            img=data["weather"][0]["icon"]
            self.WeatherImage.setPixmap(QtGui.QPixmap("images/"+img+".png"))
            temp=data["main"]["temp"]- 273.15
            self.Temp.setProperty("value",temp )
            self.description.setText(_translate("Form", data["weather"][0]["description"]))
            temp_min=data["main"]["temp_min"]- 273.15
            temp_max=data["main"]["temp_max"]- 273.15
            self.TmaxTmin.setText(_translate("Form", " T min : "+str(temp_min)+" °C    T max : "+str(temp_max)+" °C"))
            self.pressure.setText(_translate("Form", "Pressure : "+str(data["main"]["pressure"])+" hPa"))
            self.humidity.setText(_translate("Form", "Humidity : "+str(data["main"]["humidity"])+" %"))
            self.visibility.setText(_translate("Form", "Visibility : "+str(data["visibility"]/1000)+" km"))
            self.windspeed.setText(_translate("Form", "Wind : "+str(data["wind"]["speed"])+" km/h"))
            self.sunrise.setText(_translate("Form", "Sunrise : "+time.strftime('%H:%M:%S', time.localtime(data['sys']['sunrise']))))
            self.sunset.setText(_translate("Form", "Sunset : "+time.strftime('%H:%M:%S', time.localtime(data['sys']['sunset']))))
        except:
            self.description.setText(_translate("Form", "OffLine"))
 
    def vedirect_connect(self):
        # -- fonction pour connaitre sur quels ports le solar charger et le BMV-700 sont connectés
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y')
        rep=stdout.read()
        reponse = ''
        for i in range(len(rep)):
            reponse = reponse + chr(rep[i])

        biblio=reponse.split('\n')
        self.battery=''
        self.solarcharger=''

        for i in range (len(biblio)):
            c = biblio[i]
            bb = c.split('.')
            if (bb[len(bb)-1]=='ttyO2' or bb[len(bb)-1]=='ttyO4'):
                if (bb[2]=='solarcharger'):
                    self.solarcharger = c
                else :
                    self.battery = c

    def vedirect_battery(self):
        # -- fonction pour extaire les données du BMV-700
        _translate = QtCore.QCoreApplication.translate
        # Battery voltage
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.battery+' /Dc/0/Voltage GetValue')
        ch=stdout.read()
        self.Vbat=self.get_float(ch)
        self.batV.setProperty("value",self.Vbat) # a voir
        # Battery current
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.battery+' /Dc/0/Current GetValue')
        ch=stdout.read()
        self.Ibat=self.get_float(ch)
        self.batA.setProperty("value",self.Ibat) # a voir
        # Battery Power 
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.battery+' /Dc/0/Power GetValue')
        ch=stdout.read()
        self.Wbat=self.get_float(ch)
        self.batW.setProperty("value", self.Wbat)
        # Battery Soc 
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.battery+' /Soc GetValue')
        ch=stdout.read()
        self.socbat=self.get_float(ch)
        self.soc.setProperty("value",self.socbat)
        # Battery State of Relay
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.battery+' /Relay/0/State GetValue')
        ch=stdout.read()
        self.relaybat=self.get_int(ch)
        if (self.relaybat==0):
            self.batRelay.setText(_translate("Form", "OFF"))
        else:
            self.batRelay.setText(_translate("Form", "ON"))
        # Battery consumed Amp Houres
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.battery+' /ConsumedAmphours GetValue')
        ch=stdout.read()
        self.Ahbat=self.get_float(ch)
        self.batAh.setProperty("value",self.Ahbat)
        

    def vedirect_solarcharger(self):
        # -- fonction pour extaire les données de solar charger
        # PV voltage 
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.solarcharger+' /Pv/V GetValue')
        ch=stdout.read()
        self.Vsp=self.get_float(ch)
        self.spV.setProperty("value", self.Vsp)
        # PV current 
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.solarcharger+' /Pv/I GetValue')
        ch=stdout.read()
        self.Isp=self.get_float(ch)
        self.spA.setProperty("value", self.Isp)
        # PV Power 
        self.spW.setProperty("value", self.Vsp*self.Isp)
        # Load current
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.solarcharger+' /Load/I GetValue')
        ch=stdout.read()
        self.Ihome=self.get_float(ch)
        self.homeA.setProperty("value", self.Ihome)
        # Load Voltage =  Battery Voltage from solar charger
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.solarcharger+' /Dc/0/Voltage GetValue')
        ch=stdout.read()
        self.Vhome=self.get_float(ch)
        self.homeV.setProperty("value",self.Vhome) # a voir
        # Load Power
        self.homeW.setProperty("value",self.Vhome*self.Ihome)

    def battery_from_solarcharger(self):
        # -- fonction pour extaire les données concernant la batterie reliée au solar charger
        # -- en cas ou le BMV-700 n'est pas connecté.
        # Battery Voltage from solar charger 
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.solarcharger+' /Dc/0/Voltage GetValue')
        ch=stdout.read()
        self.Vbat=self.get_float(ch)
        self.batV.setProperty("value",self.Vbat) # a voir
        # Battery Current from solar charger 
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.solarcharger+' /Dc/0/Current GetValue')
        ch=stdout.read()
        self.Ibat=self.get_float(ch)
        self.batA.setProperty("value",self.Ibat) # a voir
        # Battery Power from solar charger 
        self.Wbat=self.Ibat*self.Vbat
        self.batW.setProperty("value", self.Wbat)

    def relay_state(self):
        # -- fonction pour extaire l'etat de relai
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y com.victronenergy.system /Relay/0/State GetValue')
        self.r1=self.get_int(stdout.read())
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y com.victronenergy.system /Relay/1/State GetValue')
        self.r2=self.get_int(stdout.read())
        self.on_off(self.Relay1,self.r1)
        self.on_off(self.Relay2,self.r2)

    def on_off(self,relay,state):
        # -- fonction pour changer l'image présentante l'etat du relai
        if (state==0):
            relay.setIcon(QtGui.QIcon(QtGui.QPixmap("images/off.png")))
        else:
            relay.setIcon(QtGui.QIcon(QtGui.QPixmap("images/on.png")))

    def get_float(self,chaine):
        # -- fonction pour mettre en forme la valeur reçue et la transforme en floattant
        ch=''
        for i in range(len(chaine)):
            if ((chaine[i]>=48 and chaine[i]<=57)or chaine[i]==46):
                ch=ch+chr(chaine[i])
        if (ch == ''):
            ch='0'
        return (float(ch))

    def get_int(self,chaine):
        # -- fonction pour mettre en forme la valeur reçue et la transforme en entier
        ch=''
        for i in range(len(chaine)):
            if ((chaine[i]>=48 and chaine[i]<=57)):
                ch=ch+chr(chaine[i])
        if (ch == ''):
            ch='0'
        return (int(ch))
  
    
    # --------------- actions des bouttons ------------
    
    def loginbt_on_click(self):
        if (self.login.text()=="" and self.password.text()==""):
            self.MainStackWidget.setCurrentIndex(1)
        else :
            QtWidgets.QMessageBox.warning(Form, 'Error', 'Bad Login or Password')

    def exitAppbtn_on_click(self):
        os._exit(0)

    def batterynextbtn_on_click(self):
        self.BatterystackedWidget.setCurrentIndex(1)

    def batterybackbtn_on_click(self):
        self.BatterystackedWidget.setCurrentIndex(0)
        
    def backbtn_on_click(self):
        self.MainStackWidget.setCurrentIndex(0)
	
    def overviewbt_on_click (self):
        self.MainStackWidget.setCurrentIndex(1)
	
    def plot_data(self):
        # -- fonction pour afficher le graphique 
        self.MainStackWidget.setCurrentIndex(2)
        # liste des valeurs de production et consommation :
        
        production= [0,0,0,250,500,750,1100,1200,1300,1350,1400,1700,2000,2200,2250,1900,1500,1000,600,300,100,0,0,0]
        consumption = [1000,750,750,1000,1300,1000,250,1600,1117,1437,1462,1507,3000,2125,562,475,350 ,260,210,2000,200,200,200,200]

        # preciser ou on a un surplus ou deficit d'energie :
        for i in range (len(production)):
            if production[i] > consumption[i]:
                self.graphwidget.canvas.ax.bar(i, consumption[i], bar_width,align='edge', alpha=opacity, color='gold')
                self.graphwidget.canvas.ax.bar(i, (production[i]-consumption[i]), bar_width,bottom=production[i]-(production[i]-consumption[i]),align='edge',
                       alpha=opacity, color='gold',hatch='/////',picker=True)
                self.graphwidget.canvas.ax.bar(i+0.3,consumption[i], bar_width,align='edge', alpha=opacity, color='blue')
            elif production[i]< consumption[i]:
                self.graphwidget.canvas.ax.bar(i, production[i], bar_width,align='edge', alpha=opacity, color='gold', )
                self.graphwidget.canvas.ax.bar(i+0.3, (consumption[i]-production[i]), bar_width,bottom=consumption[i]-(consumption[i]-production[i]),align='edge',
                       alpha=opacity, color='blue',hatch='/////',picker=False)
                self.graphwidget.canvas.ax.bar(i+0.3,production[i], bar_width,align='edge', alpha=opacity, color='blue',  )
       
                 
        # ajouter la legende :
        self.graphwidget.canvas.ax.bar(25, 0, bar_width,align='edge', alpha=opacity, color='gold',label='consumption')
        self.graphwidget.canvas.ax.bar(25+0.3, 0, bar_width,align='edge', alpha=opacity, color='blue',label='production')
        self.graphwidget.canvas.ax.bar(25+0.3, 0, bar_width,bottom=0,align='edge', alpha=opacity, color='blue',hatch='/////',label='surplus')
        self.graphwidget.canvas.ax.bar(25, 0, bar_width,bottom=0,align='edge', alpha=opacity, color='gold',hatch='/////',label='lack')

        # ajouter les labels :
        self.graphwidget.canvas.ax.set_xlabel('time(h)')
        self.graphwidget.canvas.ax.set_ylabel('energy(Kw/h)')
        self.graphwidget.canvas.ax.set_title('Prediction (for date of tomorrow) of energy production and consumption per hour')
        self.graphwidget.canvas.ax.set_xticks(index+0.4)
        self.graphwidget.canvas.ax.set_xticklabels(('01', '02', '03', '04','05','06','07','08','09','10','11','12','13','14',
                    '15','16','17','18','19','20','21','22','23'))
        self.graphwidget.canvas.fig.canvas.mpl_connect('pick_event', onpick1)

	
    def relay1_on_click(self):
        
        if (self.r1==0):
            self.ssh.exec_command('dbus -y com.victronenergy.system /Relay/0/State SetValue 1')
            self.Relay1.setIcon(QtGui.QIcon(QtGui.QPixmap("images/on.png")))
        else :
            self.ssh.exec_command('dbus -y com.victronenergy.system /Relay/0/State SetValue 0')
            self.Relay1.setIcon(QtGui.QIcon(QtGui.QPixmap("images/off.png")))
        
    def relay2_on_click(self):
        # -- fonction pour changer l'etat de relai
       
        if (self.r2==0):
            self.ssh.exec_command('dbus -y com.victronenergy.system /Relay/1/State SetValue 1')
            self.Relay2.setIcon(QtGui.QIcon(QtGui.QPixmap("images/on.png")))
        else :
            self.ssh.exec_command('dbus -y com.victronenergy.system /Relay/1/State SetValue 0')
            self.Relay2.setIcon(QtGui.QIcon(QtGui.QPixmap("images/off.png")))
        
     # -------------------------- mise a jour ----------------
    def update_all(self):
        self.weather_data()

        self.relay_state()
        self.vedirect_connect()
        if (self.battery == ''):
            self.battery_from_solarcharger()
        else:
            self.vedirect_battery()
        if (self.solarcharger != ''):
            self.vedirect_solarcharger()
        else:
            pass


# ***************************************************************************
# **************************************************************************

def main ():
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)

    ui.update_all
    
    Form.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
