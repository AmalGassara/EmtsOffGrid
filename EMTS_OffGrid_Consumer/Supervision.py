# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import requests
import datetime
import paramiko
global data
import time
global msg, city
import Exchange
from ExchangePlaceClasses import Prosumer, Asset
from threading import Thread
from PyQt5.QtCore import QTimer, QTime
import GenericExchangePlace
import Scheduling
msg=""
city=""

def clock(self):
    timer = QTimer(self)
    timer.timeout.connect(self.showTime)
    timer.start(10000) # update every second
    self.showTime()

def weather_data(self):
    try :
        api_address="http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
        d=Exchange.dataEnv
        city=d['localisation']
        #city="sfax"   # a changer 
        url = api_address + city
        data = requests.get(url).json()

        # -- fonction pour afficher les donn�es m�t�orologiques pour une ville : "Tunis" dans notre cas
        _translate = QtCore.QCoreApplication.translate
        #try :
        """api_address="http://api.openweathermap.org/data/2.5/weather?appid=0c42f7f6b53b244c78a418f4f181282a&q="
        city="tunis"   # a changer 
        url = api_address + city
        data = requests.get(url).json()
        #data=self.weatherData"""
        self.Localisation.setText(_translate("MainWindow", city))
        img=data["weather"][0]["icon"]
        date=datetime.datetime.fromtimestamp( data["dt"]) #1608550378
        #hour=date.strftime('%H:%M')
        #self.hour.setProperty("value",hour )
        #self.hour.setText(_translate("MainWindow", "à  "+hour))
        self.WeatherImage.setPixmap(QtGui.QPixmap("images/"+img+".png"))
        temp=data["main"]["temp"]- 273.15
        self.temperature.setProperty("value",temp )
        self.description.setText(_translate("MainWindow", data["weather"][0]["description"]))
    except:
        self.description.setText(_translate("MainWindow", "OffLine"))
        QtWidgets.QMessageBox.warning(self, 'Error', 'No connection could be established, check that the Wifi Access Point is activated and try again ...')

def updateSole(form):
    _translate = QtCore.QCoreApplication.translate
    currentProsumer=Prosumer.getInstance()
    prosumer=GenericExchangePlace.getById(GenericExchangePlace.accessToken, "prosumers", currentProsumer.idProsumer)
    sharingAccount=prosumer["sharingAccount"]
    balance=prosumer["balance"]
    form.solde.setText(_translate("MainWindow", str(balance)+"\t AU"))

class GetDataFromBC(Thread):
    def __init__(self,form, id):
        Thread.__init__(self)
        self.deamon=True
        self.id=id
        self.form=form

    def run(self):
        _translate = QtCore.QCoreApplication.translate
            
        #***************************************************************************************
        #******************************Get prosumer ********************************************
            
        prosumer=GenericExchangePlace.getById(GenericExchangePlace.accessToken, "prosumers", self.id)
        sharingAccount=prosumer["sharingAccount"]
        balance=prosumer["balance"]
        currentProsumer=Prosumer(self.id, balance, sharingAccount)
        print("currentProsumer "+ self.id)
        self.form.solde.setText(_translate("MainWindow", str(balance)+"\t AU"))
        self.form.bienvenue.setText(_translate("MainWindow", "Bienvenue "+self.id+" !"))
            
        #***************************************************************************************
        #******************************Get Asset ***********************************************
            
        result = GenericExchangePlace.getByOwner(GenericExchangePlace.accessToken, "Assets", currentProsumer.idProsumer)
        if('code' in result):
            QtWidgets.QMessageBox.information(Exchange, 'Error', str(result['message'])+'\t \t \t \t \t')
        if (type(result)==list):
            myAsset=result[0]
            myEnergyAssetId=myAsset["id"]
            myEnergyAssetDescription=myAsset["description"]
            myEnergyAssetSpecificAtt=myAsset["specificAttributes"][0]
            print(str(myEnergyAssetSpecificAtt))
            myEnergyAssetLocation=myEnergyAssetSpecificAtt["value"]
            print(str(myEnergyAssetLocation))
            myEnergyAsset=Asset(myEnergyAssetId,myEnergyAssetDescription,myEnergyAssetLocation,"energy" )
                
        #***************************************************************************************
        #******************************Get executed contracts***********************************
            
        contracts=[]
        responseJson=GenericExchangePlace.getByOwner(GenericExchangePlace.accessToken,'contracts', currentProsumer.idProsumer)
        if type(responseJson)== list:
            print(responseJson)
            #entries=[]
            contracts=responseJson
            wFeeded=0
            wConsumed=0
            for contract in contracts:
                if (contract['state']=="endDelivery"):
                    if(contract['offerer']==currentProsumer.idProsumer):
                        wFeeded=wFeeded+contract['deliveredQuantity']
                    if(contract['requestor']==currentProsumer.idProsumer):
                        wConsumed=wConsumed+contract['deliveredQuantity']
            self.form.ingoingPower.setProperty("value", wConsumed)
            self.form.outgoingPower.setProperty("value", wFeeded)

                    
        else:
            QtWidgets.QMessageBox.warning(self.form, 'Error', str(responseJson))                           
                
        #***************************************************************************************
        #******************************Listen to events ****************************************
        thread_listening=Scheduling.ListenEvent(currentProsumer,"files/tomorrowExchange.txt",Exchange.dataEnv['url_api'])
        thread_listening.start()

    

    
class GetDataFromVenus(Thread):
    def __init__(self,form):
        Thread.__init__(self)
        self.deamon=True
        self.form=form
        self.Wbat=0
        # -------------------  connection SSH -----------
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            self.target_host = Exchange.dataEnv['venusAddress']
            print(self.target_host)
            #self.target_port = 22
            self.pwd = '123456'  #, username = self.un, password = self.pwd
            self.un = 'root'
            self.ssh.connect(self.target_host, username=self.un, password = self.pwd)
            self.ssh.get_transport().window_size = 3 *1024 * 1024
            self.form.ssh=self.ssh
        except:
            QtWidgets.QMessageBox.warning(self.form, 'Error', 'No connection could be established, check that the Wifi Access Point is activated and try again ...')
        # ----------------------------------------------
    
    
    def run(self):
        while True:
            self.vedirect_connect()
            if (self.battery != ''):
                self.vedirect_battery()

            if (self.solarcharger != ''):
                self.vedirect_solarcharger()
            else:
                pass
            time.sleep(20) 
            
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
                    self.form.battery= c
    
    def vedirect_battery(self):
        print("in vedirect_battery")
        # -- fonction pour extaire les données du BMV-700
        _translate = QtCore.QCoreApplication.translate      
        # Battery Power 
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.battery+' /Dc/0/Power GetValue')
        ch=stdout.read()
        self.Wbat=self.get_float(ch)
        print("battery power value from BMV " +str(self.Wbat))
        
        #{self.form.meteringValue=self.form.meteringValue+self.Wbat
        

        if self.Wbat<0:
            self.form.wConsumed.setProperty("value",self.Wbat)
            self.form.wFeeded.setProperty("value",str(0))
            self.form.consommationPower.setProperty("value",self.Wbat)
            self.form.feededPower.setProperty("value",str(0))
        else:
            self.form.wConsumed.setProperty("value",str(0))
            self.form.wFeeded.setProperty("value",self.Wbat)
            self.form.consommationPower.setProperty("value",str(0))
            self.form.feededPower.setProperty("value",self.Wbat)
    
    def vedirect_solarcharger(self):
        # -- fonction pour extaire les données de solar charger
        # PV voltage 
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.solarcharger+' /Pv/V GetValue')
        ch=stdout.read()
        self.Vsp=self.get_float(ch)
        # PV current 
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.solarcharger+' /Pv/I GetValue')
        ch=stdout.read()
        self.Isp=self.get_float(ch)
        # PV Power 
        self.form.pvPower.setProperty("value", self.Vsp*self.Isp)#***********vérifier nom
        # Load current
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.solarcharger+' /Load/I GetValue')
        ch=stdout.read()
        self.Ihome=self.get_float(ch)
        # Load Voltage =  Battery Voltage from solar charger
        stdin, stdout, stderr = self.ssh.exec_command('dbus -y '+self.solarcharger+' /Dc/0/Voltage GetValue')
        ch=stdout.read()
        self.Vhome=self.get_float(ch)
        # Load Power
        self.form.consommationPower.setProperty("value",self.Vhome*self.Ihome) #***********vérifier nom
    
    def get_float(self,chaine):
        # -- fonction pour mettre en forme la valeur reçue et la transforme en floattant
        ch=''
        for i in range(len(chaine)):
            if ((chaine[i]>=48 and chaine[i]<=57)or chaine[i]==46 or chaine[i]==45):
                ch=ch+chr(chaine[i])
        if (ch == ''):
            ch='0'
        value=float(ch)
        return (round(value,2))

