import config
import telebot
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from models import User, Weather, Session, Base, engine
from geocoder import getPosition, getNameTown
from weatherapi import setWeather

bot = telebot.TeleBot(config.token)
DBSession = Session(bind=engine)
DBUser = DBSession.query(User)
DBWeather = DBSession.query(Weather)



@bot.message_handler(commands=["start"])
def hello(message):
  welcome = ''' Добро пожаловать в чат WeatherBot⛅️
  Что бы узнать погоду, введите название вашего города
  Доступные команды:
  /weather - кнопки'''
  bot.send_message(message.chat.id,welcome)

@bot.message_handler(commands=["weather"])
def butoon_list(message):
  keyboard = telebot.types.InlineKeyboardMarkup()
  if DBUser.filter(User.chat_id == message.from_user.id).first() != None:
    user_towns = DBUser.filter(User.chat_id == message.from_user.id).first().town.split(',')
    i = 0
    for town in user_towns:
      data_name = 'get-town'+str(i)
      keyboard.add(telebot.types.InlineKeyboardButton(town, callback_data=data_name))
      i += 1
    bot.send_message(message.chat.id,'кнопки',reply_markup=keyboard )
  else:
    bot.send_message(message.chat.id,'Вы еще не вводили города')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):

  town_name = ''
  for i in call.message.json['reply_markup']['inline_keyboard']:
    if call.data == i[0]['callback_data']:
      town_name = getNameTown(i[0]['text'])
  weather_button = DBWeather.filter_by(town=town_name).first()
  weather_message = ''' На данный момент в городе %r:
  %r
  %r°C
  ощущается как %r°C ''' % (weather_button.town,str(weather_button.condition),weather_button.temp,weather_button.feels_like)
  bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=weather_message)

@bot.message_handler(content_types=['text'])
def send_message(message):

  user = None
  try:
    name_town = getNameTown(message.text)
  except IndexError:
    bot.send_message(message.chat.id,'Такого города нет')
  # create or take a user in the database
  if DBUser.filter_by(chat_id = message.from_user.id).first() == None:
    user = User(chat_id=int(message.from_user.id))
    DBSession.add(user)
    DBSession.commit()
  else:
    user = DBUser.filter_by(chat_id=message.from_user.id).first()
  # create or take a town in the database
  if DBWeather.filter_by(town = name_town).first() == None:
    try:
      coordinates = getPosition(name_town)
      new_town = Weather(town=name_town,lat=coordinates[1],lon=coordinates[0])
      setWeather(new_town)
      DBSession.add(new_town)
      DBSession.commit()
    except IndexError:
      bot.send_message(message.chat.id,'Такого города нет')
  # add a town to the list
  if user.town == None:
    user.town = name_town
  elif user.town != None and len(user.town.split(',')) < 5 and (name_town not in str(user.town.split(','))):
    user_towns = str(user.town) + ',' + name_town
    user.town = user_towns
  elif len(user.town.split(',')) == 5 and (name_town not in str(user.town.split(','))):
    user_towns = user.town.split(',')
    user_towns[0] = name_town
    user.town = ','.join(user_towns)
  # send message with information about weather
  weather = DBWeather.filter_by(town = name_town).first()
  weather_message = ''' На данный момент в городе %r:
  %r
  %r°C
  ощущается как %r°C ''' % (str(name_town),str(weather.condition),weather.temp,weather.feels_like)
  bot.send_message(message.chat.id,weather_message)
  DBSession.commit()






if __name__ == '__main__':
     bot.polling()
