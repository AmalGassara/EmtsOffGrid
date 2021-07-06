# -*- coding: utf-8 -*-
import numpy as np
from matplotlib.figure import Figure
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.text import Text
import pyqtgraph as pg
from ExchangePlaceClasses import Prosumer, Asset

plt.style.use('ggplot')
import datetime as dt
from datetime import datetime
import Exchange
import GenericExchangePlace

def goToPrediction (self):
    bar_width = -0.3
    opacity = 0.9
    n=24
    index = np.arange(n) 
    indexY = np.arange(-70,20,10)    
    data=Exchange.dataEnv
    consumptionTable=data['consumption']
    productionTable=data['production']
    i=0
    self.consumption=[]
    self.production=[]
    sommeProduction=0
    sommeConsommation=0
    self.balance=-281.48
    if len(productionTable)!= 0 and len(consumptionTable) != 0:
        while (i<24): 
            consumptionItem=consumptionTable.split(",")[i]
            productionItem=productionTable.split(",")[i]
            self.consumption.append(float(consumptionItem))
            self.production.append(float(productionItem))
            sommeProduction=sommeProduction+ float(productionItem)
            sommeConsommation=sommeConsommation+float(consumptionItem)
            i=i+1
        print(sommeProduction)
        print(sommeConsommation)
    self.balance=sommeConsommation
    self.energyBalance.setProperty("value",self.balance)
    if(sommeProduction !=0):
        # preciser ou on a un surplus ou deficit d'energie :
        for i in range (len(self.consumption)):
            self.graphWidget.canvas.ax.bar(i,self.consumption[i], -bar_width,align='edge', alpha=opacity, color='blue')
            self.graphWidget.canvas.ax.bar(i, self.production[i],bar_width,align='edge', alpha=opacity, color='gold', )
                  
            """if self.production[i] > self.consumption[i]:
                self.graphWidget.canvas.ax.bar(i, self.consumption[i], bar_width,align='edge', alpha=opacity, color='gold')
                self.graphWidget.canvas.ax.bar(i, (self.production[i]-self.consumption[i]), bar_width,bottom=self.production[i]-(self.production[i]-self.consumption[i]),align='edge',
                        alpha=opacity, color='gold',hatch='/////',picker=True)
                self.graphWidget.canvas.ax.bar(i+0.3,self.consumption[i], bar_width,align='edge', alpha=opacity, color='blue')
            if self.production[i]< self.consumption[i]:
                self.graphWidget.canvas.ax.bar(i, self.production[i], bar_width,align='edge', alpha=opacity, color='gold', )
                self.graphWidget.canvas.ax.bar(i+0.3, (self.consumption[i]-self.production[i]), bar_width,bottom=self.consumption[i]-(self.consumption[i]-self.production[i]),align='edge',
                       alpha=opacity, color='blue',hatch='/////',picker=True)
                self.graphWidget.canvas.ax.bar(i+0.3,self.production[i], bar_width,align='edge', alpha=opacity, color='blue',  )
             """        
        # ajouter la legende :
        self.graphWidget.canvas.ax.bar(25, 0, bar_width,align='edge', alpha=opacity, color='gold',label='énergie produite du PV')
        self.graphWidget.canvas.ax.bar(25+0.3, 0, bar_width,align='edge', alpha=opacity, color='blue',label='énergie consommée/injectée au grid')
        #{self.graphWidget.canvas.ax.bar(25+0.3, 0, bar_width,bottom=0,align='edge', alpha=opacity, color='gold',hatch='/////',label='surplus')
        #self.graphWidget.canvas.ax.bar(25, 0, bar_width,bottom=0,align='edge', alpha=opacity, color='blue',hatch='/////',label='manque')
    
            # ajouter les labels :
        self.graphWidget.canvas.ax.set_xlabel('time(h)')
        self.graphWidget.canvas.ax.set_ylabel('energy(wh)')
        #self.graphWidget.canvas.ax.set_title('Prediction of energy consumption for tomorrow ')
        self.graphWidget.canvas.ax.set_xticks(index)
        self.graphWidget.canvas.ax.set_xticklabels(('01', '02', '03', '04','05','06','07','08','09','10','11','12','13','14',
                        '15','16','17','18','19','20','21','22','23','24'))
            #self.graphwidget.canvas.fig.canvas.mpl_connect('pick_event', onpick1)
        self.graphWidget.canvas.ax.legend()
        #{plt.ylim(-70, 20)
        plt.show()
    if(sommeProduction==0):
        while (i<24): 
            consumptionItem=consumptionTable.split(",")[i]
            self.consumption.append(float(consumptionItem))
            i=i+1
        # preciser ou on a un surplus ou deficit d'energie :
        for i in range (len(self.consumption)):
            self.graphWidget.canvas.ax.bar(i, self.consumption[i], 0.3,align='center', alpha=opacity, color='blue') 
        # ajouter la legende :
        self.graphWidget.canvas.ax.bar(25+0.3, 0, bar_width,align='center', alpha=opacity, color='blue',label='énergie consommée du grid')
        # ajouter les labels :
        
        self.graphWidget.canvas.ax.set_ylabel('energy(wh)')
        #self.graphWidget.canvas.ax.set_title('Prediction of energy consumption for tomorrow ')
        self.graphWidget.canvas.ax.set_yticks(indexY)
        self.graphWidget.canvas.ax.set_xlabel('time(h)')
        self.graphWidget.canvas.ax.set_xticks(index)
        self.graphWidget.canvas.ax.set_xticklabels(('01', '02', '03', '04','05','06','07','08','09','10','11','12','13','14',
                        '15','16','17','18','19','20','21','22','23', '24'))
        #self.graphwidget.canvas.fig.canvas.mpl_connect('pick_event', onpick1)
        self.graphWidget.canvas.ax.legend()
        plt.show()
        
from PyQt5 import QtWidgets
def planningOffersRequests(self):
    data=Exchange.dataEnv
    accessToken=GenericExchangePlace.accessToken
    now = dt.datetime.now()
    duree_de_un_jour = dt.timedelta(1)
    demain = now + duree_de_un_jour
    currentProsumer=Prosumer.getInstance()
    
    #if the user is a producer of solar energy (has PV panels): posting offers
    if (self.balance> 0):
        msg="Une ou plusieurs offres ont été publiées avec succés: \t  \t \n \n"
        myAsset=Asset.getInstance()
        for i in range (len(self.consumption)):
            if (self.production[i]>data['offerThreshold']):
                print('offer at '+ str(i+1) +"h")
                #post an offer "offerer,assetId,beginTimeSlot,endTimeSlot,validityLimit,offeredQuantity,price,deposit"
                offeredQuantity=abs(self.consumption[i])
                beginTime=demain.strftime("%Y-%m-%d")+"T"+'{:0=2}'.format(i+1)+":00:00.000Z" 
                print (str(beginTime))
                endTime=demain.strftime("%Y-%m-%d")+"T"+'{:0=2}'.format(i+2)+":00:00.000Z"
                print(endTime)
                price=data['exchangePlaceInfo']['price']
                deposit=data['exchangePlaceInfo']['deposit']
                cancellationFee=data['exchangePlaceInfo']['cancellationFee']
                dataToPost={"offerer":currentProsumer.idProsumer,"assetId":myAsset.assetID,"beginTimeSlot":beginTime,"endTimeSlot":endTime,"validityLimit":endTime,"offeredQuantity":offeredQuantity,"price":price,"deposit":deposit,"cancellationFee":cancellationFee}
                responseJson=GenericExchangePlace.post(accessToken,'offers', dataToPost)
                if('code' in responseJson):
                    msg=str(responseJson)
                else:
                    print(str(responseJson))
                    msg=msg+str("\t **Id de l'offre= "+str(responseJson['offerId'])+ "\t" +responseJson['message'])
                print(msg)
        if(msg=="Une ou plusieurs offres ont été publiées avec succés:\n"):
            msg="Aucune offre a été puliée \n"
        QtWidgets.QMessageBox.information(self, 'Information', msg)
        
    
    # posting requests
    if(self.balance <0):
        msgReq="Une ou plusieurs demandes ont été publiées avec succés:\n"
        for i in range (len(self.consumption)):
            if (self.consumption[i]<data['requestThreshold']):
                print('request at '+ str(i) +"h")
                requestedQuantity=abs(self.consumption[i])
                beginTime=demain.strftime("%Y-%m-%d")+"T"+'{:0=2}'.format(i+1)+":00:00.000Z" 
                print (str(beginTime))
                endTime=demain.strftime("%Y-%m-%d")+"T"+'{:0=2}'.format(i+2)+":00:00.000Z"
                print(endTime)
                price=data['exchangePlaceInfo']['price']
                deposit=data['exchangePlaceInfo']['deposit']
                location=data['exchangePlaceInfo']['location']
                dataToRequest={"requestor":currentProsumer.idProsumer,"beginTimeSlot":beginTime,"endTimeSlot":endTime,"validityLimit":endTime,
                            "transactionType":"sale/purchase","assetTypes":[{"assetTypeName":"energy","maximumPrice":price,
                            "maximumDeposit":deposit,"requestedQuantity":requestedQuantity,
                "requestedSpecificAttributes":[{"attributeName":"location","value":location,"comparisonType":"contains"}]}]}

                dataToPost={"requestor":"user2","beginTimeSlot":beginTime,"endTimeSlot":endTime,
                            "validityLimit":endTime,"transactionType":"sale/purchase","price":price,"deposit":deposit}
                responseJson=GenericExchangePlace.post(accessToken,'requests', dataToRequest)
                
                #accepting Offer
                if(len(responseJson['availableOffersIds'])!=0):
                    requestId=responseJson['requestId']
                    offerId=responseJson['availableOffersIds'][0]
                    dataToAccept={'offerId': offerId, 'requestId':requestId}
                    responseJson=GenericExchangePlace.post(accessToken,'contracts', dataToAccept)
                    
                    if("code" in responseJson):
                        msgReq=str(responseJson)
                    else:
                        idContract=responseJson['contractId']
                        print("id contract= "+ str (idContract))
                        msgReq=msgReq+str("Une offre a été acceptée: \n ** "+"Id du contract: "+str(idContract)+"\t" +responseJson['message'])+"\n"
                        #updateFile("files/toDayExchange.txt",hour, 'consumer',idContract) 
                    #update exchange Table
        if(msgReq=="Une ou plusieurs demandes ont été publiées avec succés:\n"):
            msgReq="Aucune demande a été publiée \n"
        QtWidgets.QMessageBox.information(self, 'Information', msgReq)            

