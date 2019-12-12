from models import User, Weather, Session, Base, engine
from weatherapi import setWeather
DBSession = Session(bind=engine)
dataBase = DBSession.query(Weather)
for instance in dataBase:
    print(instance.town)
    setWeather(instance)