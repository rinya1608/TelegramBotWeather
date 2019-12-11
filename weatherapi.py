from config import urlWeatherAPI, yandexKey, lang
from models import User, Weather, Session, Base, engine
from decryptions import description
import requests
import json
DBSession = Session(bind=engine)
dataBase = DBSession.query(Weather)
headers = {'X-Yandex-API-Key':yandexKey}
for instance in dataBase:
    params = {'lat':instance.lat,'lon':instance.lon}
    response = requests.get(urlWeatherAPI,params = params ,headers = headers)
    data = json.loads(response.text)
    instance.temp = data["fact"]["temp"]
    instance.feels_like = data["fact"]["feels_like"]
    instance.condition = description.get(data["fact"]["condition"])
    DBSession.commit()