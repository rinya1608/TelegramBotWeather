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
    print(data)
getPosition('Moсква')