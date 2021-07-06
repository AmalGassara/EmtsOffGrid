# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
import json
import os
import images_rc
import Scheduling
uifile_1 = 'login.ui'
form_1, base_1 = uic.loadUiType(uifile_1)

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
            # ----------------- Button actions ------        
            self.exitAppbtn.clicked.connect(self.exitAppbtn_on_click) #--- click
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
            """thread_GetDataFromBC=Supervision.GetDataFromBC(self.main,id)
            thread_GetDataFromBC.start()"""
            """thread_GetDataFromVenus=Supervision.GetDataFromVenus(self.main)
            thread_GetDataFromVenus.start()"""
            thread_executeDemo = Scheduling.readExchangeTable("files/toDayExchange.txt",self.main)
            thread_executeDemo.start()
            
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
   

if __name__ == "__main__":
    app = QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())