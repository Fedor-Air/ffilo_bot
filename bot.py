from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

from config import TOKEN

import weather_scraper as ws
import news_scraper as ns


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start", "menu"])
async def start(message: types.Message):
    start_buttons = ["Погода", "Новости"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer("Привет! Я простой telegram чат-бот, написанный на python с помощью aiogram\n Я умею:\n -повторять ваши сообщения\n -присылать прогноз погоды\n -отправлять новости\n Чтобы начать, выберите комманду:", reply_markup=keyboard)


@dp.message_handler(Text(equals="Погода"))
async def get_weather_cmd(message: types.Message):
    city_buttons = [key for key in ws.City.keys()]
    city_buttons.append("/menu")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*city_buttons)

    await message.answer("Выберите город", reply_markup=keyboard)

    @dp.message_handler(Text(equals=["Москва", "Санкт-Петербург", "Рязань", "Нижний Новгород", "Казань", "Ростов-на-Дону", "Калининград"]))
    async def get_city_name(city_name: types.Message):
        if ws.main(city_name.text)[0] == 1:
            weather_card = f"Температура: {ws.main(city_name.text)[1]}\n" \
                f"Облачность: {ws.main(city_name.text)[2]}\n" \
                f"Подробный прогноз: {ws.main(city_name.text)[3]}"
        else:
            weather_card = f"К сожалению краткий прогноз для этого города недоступен {ws.main(city_name.text)[1]}\n"

        await city_name.answer(weather_card)
        await city_name.answer("Выберите город")


@dp.message_handler(Text(equals="Новости"))
async def get_news_cmd(message: types.Message):
    news_buttons = [key for key in ns.Theme.keys()]
    news_buttons.append("/menu")
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*news_buttons)

    await message.answer("Выберите категорию", reply_markup=keyboard)

    @dp.message_handler(Text(equals=["Политика", "В мире", "Армия", "Экономика", "Общество", "Происшествия", "Наука", "Туризм", "Религия", "Культура"]))
    async def get_news_theme(theme_name: types.Message):
        for key in ns.main(theme_name.text).keys():
            news_card = f"{key} {ns.main(theme_name.text)[key]}\n"

            await theme_name.answer(news_card)
        await theme_name.answer("Выберите категорию")


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
