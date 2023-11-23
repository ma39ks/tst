import asyncio
from aiogram.utils.executor import set_webhook
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram import types
from routers.api_router import routes
from config.load_all import dp, bot
from aiohttp import web
import config.webhook_cfg as cfg
import logging
from geopy.geocoders import Nominatim
import requests


app = web.Application()
app.router.add_routes(routes)

logging.basicConfig(format=u'%(filename)+13s [LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO)

class ClientStatesGroup(StatesGroup):
    city = State()

def get_makup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Узнать погоду в текущем городе", request_location=True)
    item2 = types.KeyboardButton("Узнать погоду")
    markup.add(item1, item2, )
    return markup

@dp.message_handler(commands='cancel', state='*')
async def cancel(message: types.Message, state: FSMContext) -> None:
    await state.finish()
    await message.answer("Canceled")

@dp.message_handler(commands=["id"])
async def id_command(message: types.Message):
    await message.answer(f"ID Вашего чата: {message.chat.id}")

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.answer("Привет", reply_markup=get_makup())

# Добавляем обработчик для локации
@dp.message_handler(content_types=types.ContentTypes.LOCATION)
async def processing_geo(message: types.Message) -> None:
    lat = message.location.latitude
    lon = message.location.longitude
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.reverse((lat, lon), language="ru")
    
    if location and 'city' in location.raw['address']:
        city_name = location.raw['address']['city']
        resp = requests.get('http://web:8000/forecasts',
        params={'city': city_name}).json()
        await message.answer(f"""Прогноз на ночь:
Температура:        {resp['forecasts']['night_short']['temp']}
Скорость ветра:     {resp['forecasts']['night_short']['wind_speed']}
Давление:           {resp['forecasts']['night_short']['pressure_mm']}

Прогноз на день:
Температура:        {resp['forecasts']['day_short']['temp']}
Скорость ветра:     {resp['forecasts']['day_short']['wind_speed']}
Давление:           {resp['forecasts']['day_short']['pressure_mm']}""", reply_markup=get_makup())
    else:
        await message.answer("Не смог определить город", reply_markup=get_makup())

@dp.message_handler(lambda message: message.text == "Узнать погоду", state=None)
async def process_reply_keyboard_button(message: types.Message):
    await ClientStatesGroup.city.set()
    await message.answer("Введите название города", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=ClientStatesGroup.city)
async def processing_text(message: types.Message, state: FSMContext) -> None:
    resp = requests.get('http://web:8000/forecasts',
        params={'city': message.text}).json()
    if 'NameCityError' in resp:
        await message.answer('Неправильное имя города, попробуйте ещё раз')
        return
    print(resp)
    await message.answer(f"""Прогноз на ночь:
Температура:        {resp['forecasts']['night_short']['temp']}
Скорость ветра:     {resp['forecasts']['night_short']['wind_speed']}
Давление:           {resp['forecasts']['night_short']['pressure_mm']}

Прогноз на день:
Температура:        {resp['forecasts']['day_short']['temp']}
Скорость ветра:     {resp['forecasts']['day_short']['wind_speed']}
Давление:           {resp['forecasts']['day_short']['pressure_mm']}""", reply_markup=get_makup())
    await state.finish()

def main():
    app = web.Application(client_max_size=1024 * 1024 * 1024)
    app["bot"] = bot
    app.add_routes(routes)
    set_webhook(
        dispatcher=dp,
        webhook_path=cfg.WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        web_app=app,
    )
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(start_command, commands=["id"])
    web.run_app(app, port=cfg.WEBAPP_PORT, host=cfg.WEBAPP_HOST)

async def on_startup(dp):
    logging.warning('Bot is working...')
    await bot.set_webhook(cfg.WEBHOOK_URL)

async def on_shutdown(dp):
    logging.warning('Shutting down...')
    await bot.delete_webhook()
    logging.warning('Bye!')

async def bot_polling():
    await dp.start_polling()

async def web_app():
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, port=cfg.WEBAPP_PORT, host=cfg.WEBAPP_HOST)
    await site.start()

async def main():
    await asyncio.gather(bot_polling(), web_app())

if __name__ == '__main__':
    asyncio.run(main())