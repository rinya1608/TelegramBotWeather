from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///bot.db', echo = True)
Session = sessionmaker()
Base = declarative_base(bind=engine)


class User(Base):
    __tablename__ = 'users'
    chat_id = Column(Integer, primary_key=True)
    town = Column(Text)

    def __repr__(self):
        return 'user_id=%r, town=%r' % (self.chat_id, self.town)

class Weather(Base):
    __tablename__ = 'weather'
    town = Column(Text, primary_key=True)
    lat = Column(Text)
    lon = Column(Text)
    temp = Column(Integer)
    feels_like = Column(Integer)
    condition = Column(Text)

    def __repr__(self):
        return 'town=%r, lat=%r, lon=%r, temp=%r, feels_like=%r, condition=%r' % (self.town, 
        self.lat, self.lon, self.temp, self.feels_like, self.condition)