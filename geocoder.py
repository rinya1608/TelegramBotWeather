from config import geoCoderKey,urlCoderAPI
from models import User, Weather, Session, Base, engine
from decryptions import description
import requests
import json

DBSession = Session(bind=engine)
dataBase = DBSession.query(Weather)

def getPosition(town):
    params = {'geocode':town,'apikey':geoCoderKey, 'format':'json'}
    response = requests.get(urlCoderAPI,params = params)
    data = json.loads(response.text)
    point = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
    return point

def getNameTown(town):
    params = {'geocode':town,'apikey':geoCoderKey, 'format':'json'}
    response = requests.get(urlCoderAPI,params = params)
    data = json.loads(response.text)
    names = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['metaDataProperty']['GeocoderMetaData']['Address']['formatted'].split(', ')
    return names[len(names)-1]