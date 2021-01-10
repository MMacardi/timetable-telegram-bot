import telebot
import config
import datetime
import os, random
import pyowm
import numpy as np
from telebot import types
# import pytz 
# import tzlocal

bot = telebot.TeleBot(config.TOKEN)
owm = pyowm.OWM(config.OPEN_WEATHER_MAP_TOKEN, language = "ru")



@bot.message_handler(commands=['start'])
def send_welcome(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

	button_1 = types.KeyboardButton('Отправь фото')
	button_2 = types.KeyboardButton('Сколько времени до звонка?')

	markup.add(button_1, button_2)

	bot.reply_to(message, 
	f'''Привет <b>{message.from_user.first_name}</b>! \nЯ <b>{bot.get_me().first_name}</b>, лучший коржик в мире!
Для того чтобы узнать погоду 🌡️ ☁️, набери название города в чат.
Для другого взаимодействия используй кнопки.
\n Если кнопки отсутсвуют, пиши команды напрямую, вот список:
<b>'Сколько времени до звонка?'</b> и <b>'Отправь фото'</b>''', 
	parse_mode="html", reply_markup=markup)




@bot.message_handler(commands=['help'])
def send_docs(message):
	bot.reply_to(message, f'''Привет <b>{message.from_user.first_name}</b>! \nЯ <b>{bot.get_me().first_name}</b>, лучший коржик в мире!
Для того чтобы узнать погоду 🌡️ ☁️, набери название города в чат.
Для другого взаимодействия используй кнопки!
\n Если кнопки отсутсвуют, пиши команды напрямую, вот список:
<b>'Сколько времени до звонка?'</b> и <b>'Отправь фото'</b>''', parse_mode='html')

# logic of main activities
@bot.message_handler(content_types=['text'])
def buttons(message):

	if message.text == "Отправь фото":
		inline_markup = types.InlineKeyboardMarkup(row_width = 3)
		button_1 = types.InlineKeyboardButton("👍", callback_data = "good")
		button_2 = types.InlineKeyboardButton("👌", callback_data = "ok")
		button_3 = types.InlineKeyboardButton("👎", callback_data = "bad")

		inline_markup.add(button_1, button_2, button_3)

		path = "./static/images"
		files = os.listdir(path)
		d = random.choice(files)
		cora = open(f'static/images/{d}','rb')
		bot.send_message(message.chat.id, 'Посмотри на меня! \nЛови!', parse_mode='html' )

		bot.send_photo(message.chat.id, cora, "Ну как?", reply_markup=inline_markup)

		
	elif message.text == "Сколько времени до звонка?":
		# local_tz = pytz.timezone('Europe/Moscow')
		# def utc_to_local(utc_dt):
		# 	local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(local_tz)
		# 	return local_tz.normalize(local_dt) # .normalize might be unnecessary

		# def aslocaltimestr(utc_dt):
		# 	return utc_to_local(utc_dt).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')

		time = datetime.datetime.now()
		# in what time rings happen
		rings = [
		datetime.datetime(hour=8,minute=00,year=time.year, month=time.month, day = time.day,  second=0), 
		datetime.datetime(hour=8,minute=45,year=time.year, month=time.month, day = time.day,  second=0), 
		datetime.datetime(hour=8,minute=55,year=time.year, month=time.month, day = time.day,  second=0), 
		datetime.datetime(hour=9,minute=40,year=time.year, month=time.month, day = time.day, second=0), 
		datetime.datetime(hour=9,minute=50, year=time.year, month=time.month, day = time.day, second=0), 
		datetime.datetime(hour=10,minute=35,year=time.year, month=time.month, day = time.day, second=0), 
		datetime.datetime(hour=10,minute=50,year=time.year, month=time.month, day = time.day, second=0), 
		datetime.datetime(hour=11,minute=35,year=time.year, month=time.month, day = time.day, second=0), 
		datetime.datetime(hour=11,minute=55,year=time.year, month=time.month, day = time.day, second=0), 
		datetime.datetime(hour=12,minute=40, year=time.year, month=time.month, day = time.day, second=0),
		datetime.datetime(hour=13,minute=00,year=time.year, month=time.month, day = time.day, second=0), 
		datetime.datetime(hour=13,minute=45,year=time.year, month=time.month, day = time.day, second=0), 
		datetime.datetime(hour=14,minute=00,year=time.year, month=time.month, day = time.day, second=0), 
		datetime.datetime(hour=14,minute=45,year=time.year, month=time.month, day = time.day, second=0)
		]

		current_hour = time.hour
		current_minute = time.minute
		now = datetime.datetime(year=time.year, month=time.month, day = time.day, hour=time.hour - 3,minute=time.minute, second=time.second)
		# nearest ring to current time
		def nearest(items, pivot):
			return min(item for item in items if item > pivot)
		
		try:
			happy_sticker = open('./static/stickers/happy.tgs', 'rb')
			ring = nearest(rings, now)
			if ring > now:
				delta = ring - now
			elif now > ring:
				delta = now - ring

			mm, ss = divmod(delta.seconds, 60) # divmod is like mm = delta.seconds // 60 and ss = delta.seconds % 60
			hh, mm = divmod(mm, 60)
			time_minute = f'{time.minute}'
			ring_minute = f'{ring.minute}'

			#scenarios
	
			if hh != 0 and mm != 0 and ss != 0:
				answer =f'Осталось {hh} часов, {mm} минут и {ss} секунд.'
			elif hh == 0 and mm != 0 and ss != 0:
				answer = f'Осталось {mm} минут и {ss} секунд.'
			elif ss == 0 and mm != 0 and hh != 0:
				answer =  f'Осталось {hh} часов и {mm} минут.'
			elif ss != 0 and mm == 0 and hh != 0:
				answer =  f'Осталось {hh} часов и {ss} секунд.'
			elif hh == 0 and mm == 0 and ss != 0:
				answer = f'Осталось {ss} секунд.'
			elif hh != 0 and mm == 0 and ss == 0:
				answer =  f'Осталось {hh} часов.'
			elif hh == 0 and mm != 0 and ss == 0:
				answer =  f'Осталось {mm} минут'
			elif hh == 0 and mm == 0 and ss == 0:
				answer =  f'Сейчас!!!'
				bot.send_sticker(message.chat.id, happy_sticker)
			if ring.minute == 0:
				ring_minute = '0' + ring_minute
			if time.minute == 0 or time.minute == 1 or time.minute == 2 or time.minute == 3 or time.minute == 4 or time.minute == 5 or time.minute == 6 or time.minute == 7 or time.minute == 8 or time.minute == 9:
				time_minute = '0' + time_minute

			answer += f'\nЗвонок в <b>{ring.hour}:{ring_minute}</b> \nСейчас {time.hour}:{time_minute}'
			bot.send_message(message.chat.id, answer, parse_mode='html')
		except Exception as e:
		 	bot.send_message(message.chat.id, f'Уроки закончились!', parse_mode='html')


		

	else:
		try:
			observation = owm.weather_at_place( message.text )
			w = observation.get_weather()
			temp = w.get_temperature('celsius')["temp"]
			hum = w.get_humidity()
			time = w.get_reference_time(timeformat='iso')
			wind = w.get_wind()["speed"]

			answer ="В городе " + message.text + " сейчас " + w.get_detailed_status() + "\n"
			answer += "Температура сейчас в районе " + str(temp) + "\n\n" + "\nСкорость ветра: " + str(wind) + "м/с" + "\n" + "\nВлажность: " + str(hum) + "%" + "\n"


			bot.send_message(message.chat.id, answer)
		except Exception as e:
			bot.send_message(message.chat.id, "Не могу найти данный город. Попробуй набрать точнее 😊")

		
@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
	
	
	# images app
	if call.message:
		try:
			happy_sticker = open('./static/stickers/happy.tgs', 'rb')
			if call.data == "good":
				bot.send_sticker(call.message.chat.id, happy_sticker)
				bot.send_message(call.message.chat.id, "Спасибочки! Буду продолжать делать такие фото! Мой инстаграм: cora_corgi_dog")
			elif call.data == "ok":
				bot.send_message(call.message.chat.id, "Это хорошо! Может другая тебе больше понравится?")
			elif call.data == "bad":
				bot.send_message(call.message.chat.id, "Жалко! Может посмотришь на другие?")

			bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption="Ну как? 😊",
				reply_markup=None)

		except Exception as e:
			print(e)
	



# start
bot.polling(none_stop = True)
'''if __name__ == '__main__':
    bot.infinity_polling()'''



