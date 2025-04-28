import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.filters import CommandStart
from aiogram import F
import asyncio
import json
import pprint

# Ваш токен бота
BOT_TOKEN = "7352605219:AAFZyO9u6Ren-oI1vn8w_KGlZg3JzxvA5iU"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Логирование
logging.basicConfig(level=logging.INFO)


# Обработчик команды /start
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Привет! Пришли мне фотографию, а я обработаю её.")


# Обработчик получения фотографии
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    await message.answer("⌛ Обрабатываю фото...")  # Красивое сообщение пользователю

    # Берем самое лучшее качество фото
    photo = message.photo[-1]

    # Скачиваем фото
    file = await bot.get_file(photo.file_id)
    file_url = f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file.file_path}"

    response = requests.get(file_url)
    image_bytes = response.content

    # Готовим запрос в API
    api_url = "https://starmatch-ai.p.rapidapi.com/fetch_celebrities"
    headers = {
        "x-rapidapi-key": "9f01634ab6msh8678df376b20c2ap1876edjsn997e60a027b9",
        "x-rapidapi-host": "starmatch-ai.p.rapidapi.com",
    }

    files = {
        'file': ('photo.jpg', image_bytes, 'image/jpeg')
    }

    api_response = requests.post(api_url, headers=headers, files=files)

    if api_response.status_code == 200:
        data = api_response.json()

        # Проверяем, что data — это список
        if not isinstance(data, list) or len(data) == 0:
            await message.answer("Я не нашёл знаменитостей на фото 😢")
            return

        # Проходим по каждому найденному знаменитости
        for celeb in data:
            name = celeb.get("name", "Неизвестно")
            similarity = float(celeb.get("similarity", 0))
            image_url = celeb.get("image_url")
            wiki_url = celeb.get("wiki_url")

            caption = f"⭐ {name}\nСовпадение: {similarity:.2f}%"
            if wiki_url:
                caption += f"\n📚 [Wiki]({wiki_url})"

            if image_url:
                await message.answer_photo(photo=image_url, caption=caption, parse_mode="Markdown")
            else:
                await message.answer(caption)

    else:
        await message.answer(f"Ошибка при обработке фото: {api_response.status_code}\n{api_response.text}")



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

