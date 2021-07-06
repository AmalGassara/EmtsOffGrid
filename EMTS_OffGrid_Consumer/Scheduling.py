# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *

from PyQt5 import QtWidgets
from PyQt5 import QtGui,QtCore
import GenericExchangePlace
import Exchange
from datetime import datetime
from sseclient import SSEClient 
import json
from ExchangePlaceClasses import Prosumer
from threading import Thread
import ntplib
import time

"""global data
with open("./files/env.json") as json_file:
    data = json.load(json_file)"""
def goToTodayExchangeTable (form, file):
    with open(file, "r") as file:
        exchangeTable=file.readlines()
        lengthTable=len(exchangeTable)
        #self.tableWidget.setRowCount(lengthTable)
    i=0
    while (i<lengthTable): 
        line=exchangeTable[i].strip().split("\t")
        exchangeDirection=line[1] 
        mode=line[2] 
        contract=line[3]      
        form.todayTableWidget.setItem(i,1,QTableWidgetItem(str(exchangeDirection)))
        form.todayTableWidget.setItem(i,2,QTableWidgetItem(str(mode)))
        form.todayTableWidget.setItem(i,3,QTableWidgetItem(str(contract)))
        i=i+1
    
        
def goToTomorrowExchangeTable (form, file):
    with open(file, "r") as file:
        exchangeTable=file.readlines()
        lengthTable=len(exchangeTable)
        #self.tableWidget.setRowCount(lengthTable)
    i=0
    while (i<lengthTable): 
        line=exchangeTable[i].strip().split("\t")
        exchangeDirection=line[1] 
        mode=line[2]
        contract=line[3]      
        form.tableWidget.setItem(i,1,QTableWidgetItem(str(exchangeDirection)))
        form.tableWidget.setItem(i,2,QTableWidgetItem(str(mode)))
        form.tableWidget.setItem(i,3,QTableWidgetItem(str(contract)))
        i=i+1
        
def getSelectedContract(form, idContract,listviewName):
    accessToken=GenericExchangePlace.accessToken
    model = QtGui.QStandardItemModel()
    if(idContract != "-"):
        responseJson=GenericExchangePlace.getById(accessToken,'contracts', idContract)
        if('code' in responseJson):
                QtWidgets.QMessageBox.information(form, 'Error', str(responseJson['message'])+'\t \t \t \t \t')
        else:
            print(responseJson)
            #entries=[]
            i=responseJson
            contract= 'Contract Id: ' + idContract+'\n'+ '\t state: '+ i['state']+'\n\t price (AU per wh): '+ str(i['price']) + '\n\t deposit: '+ str(round(i['deposit'],2)) +'\n\t deliveredQuantity: '+ str(i['DeliveredQuantity']) 
            item = QtGui.QStandardItem(contract)
            model.appendRow(item)
    else:
        item = QtGui.QStandardItem("Pas de contract dans cet intervalle de temps")
        model.appendRow(item)
    #form.notificationslistWidget.addItems(entries)
    listviewName.setModel(model)

def goToContracts(form, lv):
    accessToken=GenericExchangePlace.accessToken
    contracts=[]
    model = QtGui.QStandardItemModel()
    currentProsumer=Prosumer.getInstance()
    responseJson=GenericExchangePlace.getByOwner(accessToken,'contracts', currentProsumer.idProsumer)
    if type(responseJson)== list:
        print(responseJson)
        #entries=[]
        contracts=responseJson

        for i in contracts:
            contract= 'Contract Id: ' + str(i['idContract'])+'\n'+ '\t state: '+ i['state']+ '\n\t price: '+ str(i['price']) + '\n\t deposit: '+ str(i['deposit'])+'\n\t quantityToDeliver: '+ str(i['quantityToDeliver']) +'\n\t deliveredQuantity: '+ str(i['deliveredQuantity'])+ '\n\t beginTimeSlot: '+ i['beginTimeSlot']+'\n\t endTimeSlot: '+ i['endTimeSlot'] + '\n\t effective beginTimeSlot: '+ i['effective beginTimeSlot'] +'\n\t effective endTimeSlot: '+ i['effective endTimeSlot']
            item = QtGui.QStandardItem(contract)
            model.appendRow(item)
    else:
        QtWidgets.QMessageBox.warning(form, 'Error', str(responseJson))
    #form.notificationslistWidget.addItems(entries)
    lv.setModel(model)



class ListenEvent(Thread):
    #Thread chargé à écouter les événements.
    def __init__(self,prosumer,file,url_api):
        Thread.__init__(self)
        self.deamon=True
        self.prosumer=prosumer
        self.file=file
        self.url_api=url_api

    def run(self):
        accessToken=GenericExchangePlace.accessToken
        print("in listen events")
        while True:    
            events = SSEClient(self.url_api+"events/")
            for event in events: 
                print("received event ========="+ str(event.event))
                if(str(event.event)=='acceptedOffer'):
                    msg=json.loads(event.data)
                    print(str(msg))
                    #offerer=str(msgJson.json()[1])
                    offerer=str(msg['offerer'])
                    request=GenericExchangePlace.getById(accessToken, 'requests', msg['requestId'])
                    requestor=str(request['requestor'])
                    print(requestor)
                    contractId=str(msg['contractId'])
                    if(offerer==self.prosumer.idProsumer):
                        print("update producer table")
                        contractId=msg['contractId']
                        contract=GenericExchangePlace.getById(accessToken, 'contracts', contractId)
                        date_time_obj = datetime.strptime(contract['beginTimeSlot'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        beginTimeSlot=date_time_obj.time()
                        #print('****'+str(beginTimeSlot))
                        hour=float(beginTimeSlot.strftime("%H"))
                        print("beginTimeSlot from contract" + str(hour))
                        updateFile(self.file, hour,"Communauté", "producer",contractId)
                    if(requestor==self.prosumer.idProsumer):
                        print("update consumer table")
                        contractId=msg['contractId']
                        contract=GenericExchangePlace.getById(accessToken, 'contracts', contractId)
                        date_time_obj = datetime.strptime(contract['beginTimeSlot'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        beginTimeSlot=date_time_obj.time()
                        hour=float(beginTimeSlot.strftime("%H"))
                        print("beginTimeSlot from contract" + str(hour))
                        updateFile(self.file, hour,"Communauté", "consumer", contractId)



def updateFile(file, index,exchangeWith, mode, idContract):
    with open(file, "r") as f:
        lines = f.readlines()
        #print(lines)
    with open(file,'w') as f:
        for i, line in enumerate(lines):
            if float(i+1)==index:
                if( exchangeWith == 'Communauté' and mode == 'consumer'):
                    print("in mode consumer with Communauté")
                    line=line.strip().split("\t")[0]+"\t"+ exchangeWith +"\t"+mode+"\t"+str(idContract)+'\n'
                    #{f.write(line)
                if(exchangeWith == 'Communauté' and mode =='producer'): 
                    print("in mode producer with Communauté")        
                    if(line.strip().split("\t")[1]=='Communauté' and line.strip().split("\t")[2]=='producer'):
                        contracts=line.strip().split("\t")[3]
                        line=line.strip().split("\t")[0]+"\t"+exchangeWith+"\t"+mode+"\t"+contracts+","+idContract+'\n'
                    else:
                        line=line.strip().split("\t")[0]+"\t"+exchangeWith+"\t"+mode+"\t"+idContract+'\n'
                    #f.write(line)
            f.write(line)
   
def executeDemo(form,file):             
    thread_1 = readExchangeTable(file,form)
    thread_1.start()
    
class readExchangeTable(Thread):
    #Thread charg� � lire le tableau d'�change.
    def __init__(self,file,form):
        Thread.__init__(self)
        self.deamon=True
        self.file=file
        self.form=form
        self.wbat=0
    def run(self):
        i=0
        #c = ntplib.NTPClient()
        brush = QtGui.QBrush(QtGui.QColor(0, 170, 0))
        #{brush.setStyle(QtCore.Qt.NoBrush)
        """item = QtWidgets.QTableWidgetItem()
        item.setBackground(brush)
        self.form.todayTableWidget.setStyleSheet(
           '''
           QTableView::item:selected:active {
                background: #00ff00;
            }
           '''
        )"""
        while True:
            with open(self.file, "r") as file:
                exchangeTable=file.readlines()
            #****************** PC time*****************
            current_time=time.strftime("%H:%M")
            print('From local, now is '+str(current_time))
            #*************ntp time**************
            """try:
                response = c.request('pool.ntp.org')
                local_time = time.localtime(response.tx_time)  
                current_time = time.strftime('%H:%M', local_time)
                current_time_Sec = time.strftime('%H:%M:%S', local_time)
                #nowIIns=now.strftime("%H.%M.%S")
                print('from ntp ' + current_time_Sec)
            except (ntplib.NTPException) as e:
                print('NTP client request error:', str(e))
                continue"""
            
            timeToStartReading=Exchange.dataEnv['timeToStart']  
            print(timeToStartReading)          
            if(current_time==timeToStartReading):
                _translate = QtCore.QCoreApplication.translate
                while True:
                    mode="consumer"
                    exchangeWith="Grid"
                    idContract="-"
                    try:
                        line=exchangeTable[i].strip().split("\t")
                        hour=float(line[0])
                        exchangeWith=line[1] 
                        mode=line[2] 
                        contracts=line[3] 
                        idContract=contracts.split(",")[0]
                        print('t= '+str(hour)+ ' *** '+exchangeWith+' *** '+mode+' *** ' +contracts +'****')

                        self.form.mode.setText(_translate("MainWindow", str(mode)))
                        self.form.exchangeWith.setText(_translate("MainWindow", str(exchangeWith)))
                        self.form.todayTableWidget.item(i,0).setBackground(brush)
                        self.relay_state()
                        
                        """self.form.todayTableWidget.item(i, 1).setBackground(brush)
                        print("ccccc"+idContract)
                        self.form.todayTableWidget.item(i, 2).setBackground(brush)"""
                        
                        #update contract
                        print ("consumer: etat relay1", self.r1)
                        print ("consumer: etat relay2", self.r2)
                        if(idContract != "-" and mode=="producer" and exchangeWith=="Communauté"):
                            #activate relay1
                            if (self.r1==0):
                                self.form.ssh.exec_command('dbus -y com.victronenergy.system /Relay/0/State SetValue 1')
                            if (self.r2==1):
                                self.form.ssh.exec_command('dbus -y com.victronenergy.system /Relay/1/State SetValue %0')
                            """#update contract with begin delivery  #à enlever par la suite
                            accessToken=GenericExchangePlace.accessToken
                            dataToUpdate={"state":"beginDelivery"}
                            responseJson=GenericExchangePlace.update(accessToken, "contracts/immaterialContract", idContract, dataToUpdate)
                            print(responseJson)"""
                            
                        if(idContract != "-" and mode=="consumer" and exchangeWith=="Communauté"):
                            #activate relay 2
                            if (self.r1==1):
                                self.form.ssh.exec_command('dbus -y com.victronenergy.system /Relay/0/State SetValue %0')
                            if (self.r2==0):
                                self.form.ssh.exec_command('dbus -y com.victronenergy.system /Relay/1/State SetValue 1')
                        if(idContract == "-" and exchangeWith=="Batterie"):
                            if (self.r1==1):
                                self.form.ssh.exec_command('dbus -y com.victronenergy.system /Relay/0/State SetValue %0')
                            if (self.r2==1):
                                self.form.ssh.exec_command('dbus -y com.victronenergy.system /Relay/1/State SetValue %0')
                    except: 
                        pass
                    i=i+1
                    self.vedirect_battery()
                    time.sleep(60)#en secondes                    
                    """#update contract with endDelivery
                    if(idContract != "-" and mode=="producer" and exchangeWith=="Communauté"):
                        delivredQuantity=self.wbat
                        print("deliveredQuantity "+ str(delivredQuantity))
                        accessToken=GenericExchangePlace.accessToken
                        dataToUpdate={"state":"endDelivery", "deliveredQuantity":delivredQuantity}
                        responseJson=GenericExchangePlace.update(accessToken, "contracts/immaterialContract", idContract, dataToUpdate)
                        print(responseJson)"""
                    if (i==24):
                        break
                                   
            time.sleep(1) #chaque seconde
     
    def vedirect_battery(self):
        # -- fonction pour extaire les donn�es du BMV-700
        _translate = QtCore.QCoreApplication.translate      
        # Battery Power 
        stdin, stdout, stderr = self.form.ssh.exec_command('dbus -y '+self.form.battery+' /Dc/0/Power GetValue')
        ch=stdout.read()
        self.wbat=self.get_float(ch)
        print("battery power value from ReadExchangeTable " +str(self.wbat))   
           
    def relay_state(self):
        # -- fonction pour extaire l'etat de relai
        stdin, stdout, stderr = self.form.ssh.exec_command('dbus -y com.victronenergy.system /Relay/0/State GetValue')
        self.r1=self.get_int(stdout.read())
        stdin, stdout, stderr = self.form.ssh.exec_command('dbus -y com.victronenergy.system /Relay/1/State GetValue')
        self.r2=self.get_int(stdout.read())   
    
    def get_int(self,chaine):
        # -- fonction pour mettre en forme la valeur reçue et la transforme en entier
        ch=''
        for i in range(len(chaine)):
            if ((chaine[i]>=48 and chaine[i]<=57)):
                ch=ch+chr(chaine[i])
        if (ch == ''):
            ch='0'
        return (int(ch))

    def get_float(self,chaine):
        # -- fonction pour mettre en forme la valeur re�ue et la transforme en floattant
        ch=''
        for i in range(len(chaine)):
            if ((chaine[i]>=48 and chaine[i]<=57)or chaine[i]==46 or chaine[i]==45):
                ch=ch+chr(chaine[i])
        if (ch == ''):
            ch='0'
        value=float(ch)
        return (round(value,2))
