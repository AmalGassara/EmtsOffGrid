class Prosumer(object):
    __instance=None
    
    @staticmethod
    def getInstance():
        return Prosumer.__instance
    
    def __init__(self, idProsumer=None, balance=None, sharingAccount= None):
        self.idProsumer=idProsumer
        self.balance=balance
        self.sharingAccount=sharingAccount
        Prosumer.__instance=self
        

class Asset(object):
    __instance=None
    
    def __init__(self, assetID, description,location, assetType):
        self.assetID=assetID
        self.description=description
        #{self.quantity=quantity
        self.location=location
        self.assetType=assetType
        Asset.__instance=self
        
    @staticmethod
    def getInstance():
        return Asset.__instance 