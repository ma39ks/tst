import requests
import os


# lat = 0
# lon = 0
# h = {
#     'X-Yandex-API-Key': os.environ.get('YaWeatherKey')
# }
# response = requests.get(f'https://api.weather.yandex.ru/v2/forecast/?lat={lat}&lon={lon}&lang=ru_RU', headers=h)





from geopy.geocoders import Nominatim

def get_city_name(lat, lon):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.reverse((lat, lon), language="ru")
    
    if location and 'city' in location.raw['address']:
        city_name = location.raw['address']['city']
        return city_name
    else:
        return None

# Пример использования
latitude = 55.751244  # Широта (например, Москва)
longitude = 37.618423  # Долгота

city_name = get_city_name(latitude, longitude)
print(city_name)












# import logging
# import os

# from aiogram import types, Dispatcher, Bot
# from aiogram.types import WebAppInfo
# from dotenv import load_dotenv
# from fastapi import FastAPI
# from fastapi.responses import FileResponse

# load_dotenv()

# TOKEN = os.environ["TELEGRAM_TOKEN"]
# BACK_URL = os.environ["BACK_URL"]
# REACT_URL = os.environ["REACT_URL"]

# WEBHOOK_PATH = f"/bot/{TOKEN}"
# WEBHOOK_URL = BACK_URL + WEBHOOK_PATH

# bot = Bot(token=TOKEN)
# dp = Dispatcher(bot)

# app = FastAPI()

# favicon_path = 'favicon.ico'


# @app.get('/favicon.ico', include_in_schema=False)
# async def favicon():
#     return FileResponse(favicon_path)


# @app.get("/")
# async def root():
#     return {"message": "Hello habr"}


# @app.on_event("startup")
# async def on_startup():
#     webhook_info = await bot.get_webhook_info()
#     if webhook_info.url != WEBHOOK_URL:
#         await bot.set_webhook(
#             url=WEBHOOK_URL
#         )


# @app.post(WEBHOOK_PATH)
# async def bot_webhook(update: dict):
#     telegram_update = types.Update(**update)
#     Dispatcher.set_current(dp)
#     Bot.set_current(bot)
#     await dp.process_update(telegram_update)


# @app.on_event("shutdown")
# async def on_shutdown():
#     await bot.get_session()
#     await bot.session.close()
#     logging.info("Bot stopped")


# @dp.message_handler(commands="start")
# async def new_message(message: types.Message):
#     text = 'REACT'
#     keyboard = types.InlineKeyboardMarkup()
#     keyboard.add(types.InlineKeyboardButton('Launch react', web_app=WebAppInfo(url=REACT_URL)))
#     await bot.send_message(message.chat.id, text, reply_markup=keyboard)


# @app.post(WEBHOOK_PATH)
# async def bot_webhook(update: dict):
#     telegram_update = types.Update(**update)
#     Dispatcher.set_current(dp)
#     Bot.set_current(bot)
#     await dp.process_update(telegram_update)