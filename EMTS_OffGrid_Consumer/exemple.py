import requests
import json
import logging
from sseclient import SSEClient 

url_api="http://192.168.1.8:10010/"
url_OAuth="http://192.168.1.8:4000/oauth/api/v1.0.0/auth/sign_in"



logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(funcName)s() -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
)

#Sign_in via the authentification server
def signIn(username, password):
        headers={"accept": "application/json", "Content-Type": "application/json"}
        data=json.dumps({"userName":username,"password":password})
        response=requests.post(url_OAuth, headers=headers, data=data)
        if (response.status_code==200):
            accessToken=response.json()["accessToken"]
            logging.info('accessToken: '+accessToken)
            return accessToken   
        else:
            logging.warning(response.text)
            return "An error has occured"

#Call a POST request of the Exchange place RestApi
def post(accessToken, item, data):
    url=url_api+item
    headers={"accept": "application/json", "Content-Type": "application/json","Authorization":'Bearer {}'.format(accessToken)}
    response=requests.post(url, headers=headers, data=json.dumps(data))
    if(response.status_code==200):
        logging.info (response.json())
    else:
        logging.warning(response.json())
    return response.json() #verify for buy


#Call a GET all request of the Exchange place RestApi
def getAll(accessToken, item):
    url= url_api+item
    headers={"accept": "application/json","Authorization":'Bearer {}'.format(accessToken)}
    response = requests.get(url, headers=headers)
    if (response.status_code==200):
        logging.info(response.text)
    else:
        logging.warning(response.text)
    return response.json()

#Call a GET by Id request of the Exchange place RestApi
def getById(accessToken, item, id):
    url= url_api+item+"/"+id
    headers={"accept": "application/json","Authorization":'Bearer {}'.format(accessToken)}
    response = requests.get(url, headers=headers)
    if (response.status_code==200):
        logging.info(response.text)
    else:
        logging.warning(response.text)
    return response.json()

#Call a delete request of the Exchange place RestApi
def delete(accessToken, item, id):
    url= url_api+item+"/"+id
    headers={"accept": "application/json","Authorization":'Bearer {}'.format(accessToken)}
    response = requests.delete(url, headers=headers)
    if (response.status_code==200):
        logging.info(response.text)
    else:
        logging.warning(response.text)
    return response.json()
   
#Call an update request of the Exchange place RestApi
def update(accessToken, item, id, data):
    url= url_api+item+"/"+id
    headers={"accept": "application/json", "Content-Type": "application/json","Authorization":'Bearer {}'.format(accessToken)}
    response = requests.patch(url, headers=headers,data=json.dumps(data))
    if (response.status_code==200):
        logging.info(response.text)
    else:
        logging.warning(response.text)
    return response.json()
#subscribe to events
def subscribeToEvents():
    events = SSEClient(url_api+"events/")
    for event in events: 
        msg=json.loads(event.data)
        logging.info('an event  is received:\n'+ msg)
            
username = 'admin'
password = 'admin123'
#access_token = signIn(username, password)

"""data = {
  "id": "test",
  "sharingAccount": 100,
  "balance": 1000
}
post(access_token, 'prosumers','user1',data)"""
#delete(access_token,'prosumers', 'test')
#getAll(access_token,'prosumers')
#getById(access_token,'prosumers', 'user')
"""data = {
  "accountUnits": 1000
}
update(access_token, 'prosumers','user1',data)"""
subscribeToEvents() 