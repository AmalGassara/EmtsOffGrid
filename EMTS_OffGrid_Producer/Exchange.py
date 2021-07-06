# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox

import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os
import math
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
from pip._internal import req
from ExchangePlaceClasses import Prosumer, Asset

import json
import Scheduling, Supervision, GenericExchangePlace, Prediction

global dataEnv
with open("./files/env.json") as json_file:
    dataEnv = json.load(json_file)
    

uifile_2 = 'Exchange.ui'
form_2, base_2 = uic.loadUiType(uifile_2)
import images_rc

##############

class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        Canvas.__init__(self, self.fig)
        """Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)"""
               
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   
        self.canvas = MplCanvas()                  
        self.vbl = QtWidgets.QVBoxLayout()         
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
######################################

class Exchange(base_2, form_2):
    __instance = None
    def __init__(self):
        """ Virtually private constructor. """
        if Exchange.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            super(base_2, self).__init__()
            self.setupUi(self) 
            Supervision.weather_data(self)
            Supervision.clock(self)
            self.battery=''
            self.ssh=''
            self.graphWidget = MplWidget(self.page_2)
            self.graphWidget.setGeometry(QtCore.QRect(10, 155, 871, 340))
            self.graphWidget.setObjectName("graphWidget")
            self.actionPREVIISIION.triggered.connect(self.goToPrediction)
            self.actionMAINTENANT.triggered.connect(self.goToSupervision)
            self.actionAujourd_hui.triggered.connect(self.goToTodayExchangeTable)
            self.actionDemain.triggered.connect(self.goToTomorrowExchangeTable)
            self.actionRe_ues.triggered.connect(self.goToNotifications)
            self.planificationButton.clicked.connect(self.goToPlanning)
            self.todayTableWidget.itemClicked.connect(self.goToTodayContractDetails)
            self.tableWidget.itemClicked.connect(self.goToTomorrowContractDetails)
        Exchange.__instance = self

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Exchange.__instance == None:
            Exchange()
        return Exchange.__instance 
    
    def goToTodayContractDetails(self):
        indexes = self.todayTableWidget.selectionModel().selectedRows()
        for index in sorted(indexes): 
            print('contract id is selected' + self.todayTableWidget.item(index.row(), 3).text())
            idContracts=self.todayTableWidget.item( index.row(), 3).text()
            idContract=idContracts.split(",")[0]
            Scheduling.getSelectedContract(self, idContract,self.contractlistView)
    def goToTomorrowContractDetails(self):
        indexes = self.tableWidget.selectionModel().selectedRows()
        for index in sorted(indexes): 
            print('contract id is selected' + self.tableWidget.item(index.row(), 3).text())
            idContracts=self.tableWidget.item( index.row(), 3).text()
            idContract=idContracts.split(",")[0]
            Scheduling.getSelectedContract(self, idContract, self.contractslistView)
            
    def doit(self):
        print ("Opening a new popup window...")
        """self.splash=QSplashScreen(QtGui.QPixmap('./images/localisation.jpg'))
        self.splash.showMessage( "nouvelle notification", Qt.AlignTop | Qt.AlignLeft )
        self.splash.show()"""
        self.splashLabel = QtWidgets.QWidget()
        self.splashLabel.setWindowFlags(Qt.SplashScreen | Qt.FramelessWindowHint)
        #self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        resolution = QDesktopWidget().screenGeometry(-1)
        screenWidth = resolution.width()
        screenHeight = resolution.height()
        print("width: " + str (self.MainStackWidget.x()) + " height: " + str(resolution.height()))
        self.splashLabel.setGeometry(QRect(0, 0, 300, 51))
        self.splashLabel.show()
        #self.w.setGeometry(QRect(0, 0, 341, 51))
        #self.splash.move(10,10)
        #self.w.setParent(self.centralwidget)
        #self.w.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
        """self.w = MyPopup()
        self.w.setWindowFlags(QtCore.Qt.SplashScreen)
        self.w.messageLabel = QLabel("nouvelle notification", self.w)
        self.w.messageLabel.setStyleSheet(
            "font-family: 'Roboto', sans-serif; font-size: 12px; font-weight: normal; padding: 0;")
        self.w.show()"""
        # Close SplashScreen after 3 seconds (3000 ms)
        QTimer.singleShot(3000, self.splashLabel.close)
        #QtWidgets.QMessageBox.information(self, 'Error', str(msg)+'\t \t \t \t \t')
        """msg = QMessageBox()
        msg.setWindowTitle("")
        msg.setText("This is the main text!")
        x = msg.exec_()"""
     
    def goToSupervision (self):     
        self.MainStackWidget.setCurrentIndex(0)
        
        Supervision.updateSole(self)
        
    def goToPrediction (self):
        self.MainStackWidget.setCurrentIndex(1)
        Prediction.goToPrediction(self)
        
    def goToTodayExchangeTable (self):
        self.MainStackWidget.setCurrentIndex(3)
        Scheduling.goToTodayExchangeTable(self, "files/toDayExchange.txt")
        #Scheduling.goToContracts(self,self.listView)
    def goToTomorrowExchangeTable (self):
        self.MainStackWidget.setCurrentIndex(2)
        Scheduling.goToTomorrowExchangeTable(self, "files/tomorrowExchange.txt")
        #Scheduling.goToContracts(self,self.contractslistView)

    def goToNotifications (self):
        entries = ['one\n ones','two', 'three']
        model = QtGui.QStandardItemModel()
        for i in entries:
            item = QtGui.QStandardItem(i)
            model.appendRow(item)
        #self.notificationslistView.addItems(entries)
        self.notificationslistView.setModel(model)
        #self.notificationslistView.setStyleSheet("background-color:rgb(0, 0, 0);")
        self.MainStackWidget.setCurrentIndex(4)
    def goToPlanning(self):
        Prediction.planningOffersRequests(self)
        
    def executeDemo(self):
        Scheduling.executeDemo(self,"files/toDayExchange.txt")
    
    def showTime(self):
        currentTime = QTime.currentTime()
        displayTxt = currentTime.toString('hh:mm')
        _translate = QtCore.QCoreApplication.translate
        self.hour.setText(_translate("MainWindow", "à  "+displayTxt))
