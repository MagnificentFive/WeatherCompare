import requests
import xmltodict
import datetime
from config import tg_bot_token, open_weather_token, news_api
from config import admin_chat_id
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

class Form(StatesGroup):
    weather = State()  # Will be represented in storage as 'Form:weather'
    news = State()

storage = MemoryStorage()

bot = Bot(token=f'{tg_bot_token}')
dp = Dispatcher(bot, storage=storage)

@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    data_of_user = [message.from_user.first_name, message.chat.id, message.from_user.id, message.from_user.username]
    requests.post(f'https://api.telegram.org/{tg_bot_token}/sendMessage?chat_id={admin_chat_id}'
                      f'&text=Новый пользователь {data_of_user[0], data_of_user[1]}')
    start_message_text = f'Здравствуйте, {message.from_user.first_name}! ' \
                         f'Напишите мне /menu и я пришлю возможные варианты!'\
    
    await bot.send_message(message.chat.id, text=start_message_text)


@dp.message_handler(commands=['menu'])
async def start_message(message: types.Message):
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    more_btns_text = (
        "Погода",
        "Новости",
        "Курс валют"
    )
    menu_keyboard.add(*(types.KeyboardButton(text) for text in more_btns_text))
    await bot.send_message(message.chat.id, text='Выберите пункт меню:', reply_markup=menu_keyboard)


@dp.message_handler(text=['Погода'])
async def add_user(message: types.Message):
    await Form.weather.set()
    await message.reply(" Напиши мне название города и я пришлю сводку погоды!")

@dp.message_handler(state=Form.weather)
async def get_weather(message: types.Message, state: FSMContext):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Облачно \U00002601",
        "Rain": "Дождь \U00002614",
        "Drizzle": "Дождь \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Снег \U0001F328",
        "Mist": "Туман \U0001F32B"
    }

    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric"
        )
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]

        weather_description = data["weather"][0]["main"]
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind = data["wind"]["speed"]
        sunrise_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
        sunset_timestamp = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
        length_of_the_day = datetime.datetime.fromtimestamp(data["sys"]["sunset"]) - datetime.datetime.fromtimestamp(
            data["sys"]["sunrise"])
        await state.finish()
        await message.reply(f"***{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}***\n"
              f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
              f"Влажность: {humidity}%\nДавление: {pressure} мм.рт.ст\nВетер: {wind} м/с\n"
              f"Восход солнца: {sunrise_timestamp}\nЗакат солнца: {sunset_timestamp}\nПродолжительность дня: {length_of_the_day}\n"
              f"***Хорошего дня!***"
              )

    except:
        await state.finish()
        await message.reply("\U00002620 Проверьте название города \U00002620")

@dp.message_handler(text='Новости')
async def get_weather(message: types.Message):
    try:
        req = requests.get(url=f'https://newsapi.org/v2/top-headlines?country=ru&category=technology&apiKey={news_api}')

        #print(req)
        news_list =[]
        req_json = req.json()
        #print(req_json)
        for i in range (6):
            data=req_json['articles'][int(i)]['title']
            await bot.send_message(message.chat.id, text=data)
        #print(req_json['articles'][int(i)]['title'])
        #print()

    except Exception as e:
        #await message.reply(e)
        await message.reply("Ошибка в запросе новостей, попробуйте позже")

@dp.message_handler(text='Курс валют')
async def get_weather(message: types.Message):
    try:
        def currency():
            req = requests.get('http://www.cbr.ru/scripts/XML_daily.asp')
            xmldict = xmltodict.parse(req.text, encoding='utf-8')
            # print(xmldict['ValCurs']['Valute'][0])
            data = f''
            for val in xmldict['ValCurs']['Valute']:
                if val['@ID'] == 'R01235' or \
                        val['@ID'] == 'R01239' or \
                        val['@ID'] == 'R01375':
                    # print(val)
                    data += val['CharCode'] + ' ' + str(round(float(val['Value'].replace(',', '.')), 2)) + '\n'
            return data
        data=currency()
        await bot.send_message(message.chat.id, text=data)
        #print(req_json['articles'][int(i)]['title'])
        #print()

    except Exception as e:
        #await message.reply(e)
        await message.reply("Ошибка в запросе курсов валют, попробуйте позже")


@dp.message_handler(state='*', commands=['cancel', 'отмена'])
@dp.message_handler(Text(equals=['cancel', 'отмена'], ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    more_btns_text = (
        "Погода",
        "Новости",
    )
    menu_keyboard.add(*(types.KeyboardButton(text) for text in more_btns_text))
    await bot.send_message(message.chat.id, text='Запрос погоды отменен. Выберите пункт меню:',
                           reply_markup=menu_keyboard)

if __name__ == '__main__':
    executor.start_polling(dp)