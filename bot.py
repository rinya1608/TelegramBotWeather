import config
import telebot
from pyramid.config import Configurator
from pyramid.response import Response
from models import User, Weather, Session, Base, engine

bot = telebot.TeleBot(config.token)
DBSession = Session(bind=engine)
DBUser = DBSession.query(User)
DBWeather = DBSession.query(Weather)
@bot.message_handler(commands=["start"])
def hello(message):
  welcome = ''' Добро пожаловать в чат WeatherBot⛅️
  Что бы узнать погоду, введите название вашего города
  Доступные команды:
  /list - Доступные города🏙'''
  bot.send_message(message.chat.id,welcome)

@bot.message_handler(commands=["list"])
def list_of_town(message):
  all_town = 'Cписок доступных городов:\n'
  data = DBSession.query(Weather).order_by(Weather.town)
  for instance in data:
    all_town +=instance.town + '\n'
  bot.send_message(message.chat.id,all_town)

@bot.message_handler(content_types=['text'])
def send_message(message):
  if message.chat.id not in DBUser:
    new_user = User(chat_id=int(message.from_user.id))
    DBSession.add(new_user)
    DBSession.commit()
    print(message.from_user.id)





if __name__ == '__main__':
     bot.polling()
