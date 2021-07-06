# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
import json
import os
import images_rc
import Scheduling
uifile_1 = 'login.ui'
form_1, base_1 = uic.loadUiType(uifile_1)
uifile_2 = 'Exchange.ui'
form_2, base_2 = uic.loadUiType(uifile_2)
from Exchange import Exchange
import GenericExchangePlace, Supervision
import sys
from ExchangePlaceClasses import Prosumer, Asset 

global dataEnv
with open("./files/env.json") as json_file:
    dataEnv = json.load(json_file)

class Login(base_1, form_1):    
    __instance = None
    def __init__(self):    
        """ Virtually private constructor. """
        if Login.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            super(base_1,self).__init__()
            self.setupUi(self)
            Login.__instance = self
            self.loginbt.clicked.connect(self.change)
  
    @staticmethod 
    def getInstance():
        """ Static access method. """
        if Login.__instance == None:
            Login()
        return Login.__instance    
    
    def change(self):
        id=self.login.text()
        pw=self.password.text()
        
        if(self.loginBC(id,pw)==True):       
            self.main = Exchange.getInstance()
            self.main.show()
            self.close()
            thread_GetDataFromBC=Supervision.GetDataFromBC(self.main,id)
            thread_GetDataFromBC.start()
            #thread_GetDataFromVenus=Supervision.GetDataFromVenus(self.main)
            #thread_GetDataFromVenus.start()
            #{currentProsumer=Prosumer.getInstance()
            """prosumer=GenericExchangePlace.getById(GenericExchangePlace.accessToken, "prosumers", id)
            sharingAccount=prosumer["sharingAccount"]
            balance=prosumer["balance"]
            currentProsumer=Prosumer(id, balance, sharingAccount)
            print("currentProsumer "+ id)
            result = GenericExchangePlace.getByOwner(GenericExchangePlace.accessToken, "Assets", currentProsumer.idProsumer)
            if('code' in result):
                QtWidgets.QMessageBox.information(Exchange.getInstance(), 'Error', str(result['message'])+'\t \t \t \t \t')
            if (type(result)==list):
                myAsset=result[0]
                myEnergyAssetId=myAsset["id"]
                myEnergyAssetDescription=myAsset["description"]
                myEnergyAssetSpecificAtt=myAsset["specificAttributes"][0]
                print(str(myEnergyAssetSpecificAtt))
                myEnergyAssetLocation=myEnergyAssetSpecificAtt["value"]
                print(str(myEnergyAssetLocation))
                myEnergyAsset=Asset(myEnergyAssetId,myEnergyAssetDescription,myEnergyAssetLocation,"energy" )
            thread_listening=Scheduling.ListenEvent(currentProsumer,"files/tomorrowExchange.txt",dataEnv['url_api'])
            thread_listening.start()"""
            
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', "nom d'utilisateur ou mot de passe incorrecte") 

    def loginBC(self, id,pw):
        GenericExchangePlace.accessToken=GenericExchangePlace.signIn(id,pw)
        if(GenericExchangePlace.accessToken=='An error has occured'):
            print('authentication failed')
            return False
        else:    
            print("the connected prosumer id ="+ id)
            
            return True  



    def exitAppbtn_on_click(self):
        os._exit(0)
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1018, 605)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 170, 170))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 127, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        Form.setPalette(palette)
        Form.setAutoFillBackground(True)
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(0, 0, 1021, 611))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(28)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("background-image:url(:/images/background1.png)")
        self.label_12.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_12.setObjectName("label_12")
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(142, 271, 561, 241))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.groupBox.setFont(font)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 46, 171, 51))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(10, 111, 171, 50))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.login = QtWidgets.QLineEdit(self.groupBox)
        self.login.setGeometry(QtCore.QRect(180, 46, 371, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.login.setFont(font)
        self.login.setStyleSheet("border-radius: 15px;border: 2px solid gray;")
        self.login.setObjectName("login")
        self.password = QtWidgets.QLineEdit(self.groupBox)
        self.password.setGeometry(QtCore.QRect(180, 111, 371, 50))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.password.setFont(font)
        self.password.setStyleSheet("border-radius: 15px;border: 2px solid gray;")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.loginbt = QtWidgets.QPushButton(self.groupBox)
        self.loginbt.setGeometry(QtCore.QRect(190, 180, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(20)
        self.loginbt.setFont(font)
        self.loginbt.setStyleSheet("border-radius: 20px;color: rgb(0, 0, 0);background-color: rgb(24, 154, 214);")
        self.loginbt.setObjectName("loginbt")
        self.exitAppbtn = QtWidgets.QPushButton(self.groupBox)
        self.exitAppbtn.setGeometry(QtCore.QRect(380, 180, 150, 50))
        font = QtGui.QFont()
        font.setFamily("Gill Sans MT")
        font.setPointSize(20)
        self.exitAppbtn.setFont(font)
        self.exitAppbtn.setStyleSheet("border-radius: 20px;color: rgb(0, 0, 0);background-color: rgb(24, 154, 214);")
        self.exitAppbtn.setObjectName("exitAppbtn")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(60, 110, 491, 161))
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
       # ----------------- Button actions ------        
        
        self.exitAppbtn.clicked.connect(self.exitAppbtn_on_click) #--- click

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_12.setText(_translate("Form", "<html><head/><body><p><br/>Place d\'échange d\'énergie</p></body></html>"))
        self.groupBox.setTitle(_translate("Form", "Se connecter"))
        self.label.setText(_translate("Form", "<html><head/><body><p>Nom de l\'utilisateur</p></body></html>"))
        self.label_10.setText(_translate("Form", "Mot de passe"))
        self.loginbt.setText(_translate("Form", "Ok"))
        self.exitAppbtn.setText(_translate("Form", "Annuler"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p align=\"justify\"><span style=\" font-size:16pt;\">- Echanger une énergie verte produite localement</span></p><p align=\"justify\"><span style=\" font-size:16pt;\">- Gérer efficacement la production d’énergie verte</span></p><p align=\"justify\"><span style=\" font-size:16pt;\">- Accéder à une énergie verte locale moins chère</span></p></body></html>"))

def connect(id):
    prosumer=GenericExchangePlace.getById(GenericExchangePlace.accessToken, "prosumers", id)
    sharingAccount=prosumer["sharingAccount"]
    balance=prosumer["balance"]
    currentProsumer=Prosumer(id, balance, sharingAccount)
    print("currentProsumer "+ id)
    result = GenericExchangePlace.getByOwner(GenericExchangePlace.accessToken, "Assets", currentProsumer.idProsumer)
    if('code' in result):
        QtWidgets.QMessageBox.information(Exchange.getInstance(), 'Error', str(result['message'])+'\t \t \t \t \t')
    if (type(result)==list):
        myAsset=result[0]
        myEnergyAssetId=myAsset["id"]
        myEnergyAssetDescription=myAsset["description"]
        myEnergyAssetSpecificAtt=myAsset["specificAttributes"][0]
        print(str(myEnergyAssetSpecificAtt))
        myEnergyAssetLocation=myEnergyAssetSpecificAtt["value"]
        print(str(myEnergyAssetLocation))
        myEnergyAsset=Asset(myEnergyAssetId,myEnergyAssetDescription,myEnergyAssetLocation,"energy" )
    thread_listening=Scheduling.ListenEvent(currentProsumer,"files/tomorrowExchange.txt",dataEnv['url_api'])
    thread_listening.start()   

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())