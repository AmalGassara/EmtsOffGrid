import requests
import json
import logging
from sseclient import SSEClient 
import Exchange

accessToken="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1ZmYzMzU2NWM2NjE2YzYwN2Y3MmFmMzQiLCJpYXQiOjE2MTUxOTE0NjUsImV4cCI6MTYxNTE5ODY2NX0.oq3rfATEKixp_l3N5tjrHhi_hVT4wqjL04qrf3oKI5M"



"""data=Exchange.dataEnv
url_api=data['url_api']
url_Oauth=data['url_OAuth']"""

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(funcName)s() - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO)

#Sign_in via the authentication server
def signIn(username, password):
    data=Exchange.dataEnv
    url_Oauth=data['url_OAuth']
    headers={"accept": "application/json", "Content-Type": "application/json"}
    data=json.dumps({"userName":username,"password":password})
    response=requests.post(url_Oauth, headers=headers, data=data)
    if (response.status_code==200):
        accessToken=response.json()["accessToken"]
        logging.info('accessToken: '+accessToken)
        return accessToken   
    else:
        logging.warning(response.text)
        return "An error has occured"

#Call a GET by owner request of the Exchange place RestApi
def getByOwner(accessToken, resource, idOwner):
    data=Exchange.dataEnv
    url_api=data['url_api']
    print(url_api)
    print(accessToken)
    url= url_api+ resource+ "/owner/"+ idOwner
    headers={"accept": "application/json","Authorization":'Bearer {}'.format(accessToken)}
    response = requests.get(url, headers=headers)
    if (response.status_code==200):
        logging.info(response.text)
    else:
        logging.warning(response.text)
    return response.json()

# Call a POST request of the Exchange place RestApi
def post(accessToken, resource, dataToPost):
    data=Exchange.dataEnv
    url_api=data['url_api']
    print(url_api)
    url=url_api + resource
    headers={"accept": "application/json", "Content-Type": "application/json", "Authorization":'Bearer {}'.format(accessToken)}
    response=requests.post(url, headers=headers, data=json.dumps(dataToPost))
    if(response.status_code==200):
        logging.info (response.json())
    else:
        logging.warning(response.json())
    return response.json()

#Call a GET by Id request of the Exchange place RestApi
def getById(accessToken, resource, id):
    data=Exchange.dataEnv
    url_api=data['url_api']
    url= url_api+ resource+ "/"+ id
    headers={"accept": "application/json","Authorization":'Bearer {}'.format(accessToken)}
    response = requests.get(url, headers=headers)
    if (response.status_code==200):
        logging.info(response.text)
    else:
        logging.warning(response.text)
    return response.json()

#Call an update request of the Exchange place RestApi
def update(accessToken, item, id, dataToUpdate):
    data=Exchange.dataEnv
    url_api=data['url_api']
    url= url_api+item+"/"+id
    headers={"accept": "application/json", "Content-Type": "application/json","Authorization":'Bearer {}'.format(accessToken)}
    response = requests.patch(url, headers=headers,data=json.dumps(dataToUpdate))
    if (response.status_code==200):
        logging.info(response.text)
    else:
        logging.warning(response.text)
    return response.json()

def connectToSolcast():
    url="https://api.solcast.com.au/world_radiation/estimated_actuals?latitude=34.843794&longitude=10.762381&hours=168&api_key=VdyKA-jrSlIh03g7_RD-HWt-gxz-EWtc"
    headers={"accept": "application/json"}
    data=json.dumps({"latitude":34.843794,"longitude":10.762381, "hours":168})
    response=requests.get(url, headers=headers)
    print('go')
    if (response.status_code==200):
        print('ok')
        
        logging.info('accessToken: '+str(response.json()))
        print(type(response.json()))
        return accessToken   
    else:
        print('not ok')
        logging.warning("hhhhh"+response.text)
        return "An error has occured"
def connectToSolarGis():
    request_xml = '''<ws:dataDeliveryRequest dateFrom="2021-01-11" dateTo="2021-01-11"
    xmlns="http://geomodel.eu/schema/data/request"
    xmlns:ws="http://geomodel.eu/schema/ws/data"
    xmlns:geo="http://geomodel.eu/schema/common/geo"
    xmlns:pv="http://geomodel.eu/schema/common/pv"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
    <site id="demo_site" name="Demo site" lat="34.843794" lng="10.762381">
    </site>
    <processing key="GHI" summarization="HOURLY" terrainShading="true">
    </processing>
    </ws:dataDeliveryRequest>'''
    api_key = 'demo'
    url = 'https://solargis.info/ws/rest/datadelivery/request?key=%s' % api_key
    headers = {'Content-Type': 'application/xml'}
    with requests.post(url, data=request_xml.encode('utf8'), headers=headers) as response:
        print(response.text)
        # parse and consume successful response, or inspect error code and a message from the server
