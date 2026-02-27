import requests
from aiogram import Bot, Dispatcher, types

from config import BOT_TOKEN, ADMINS, API_URL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def is_admin(user_id):
    return user_id in ADMINS


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("Нет доступа.")
        return

    await message.answer(
        "Бот поддержки.fm\n\n"
        "Формат добавления:\n"
        "/add <url> | <title>"
    )


@dp.message_handler(commands=["add"])
async def add_track(message: types.Message):
    if not is_admin(message.from_user.id):
        return

    try:
        args = message.get_args()

        if "|" not in args:
            await message.answer(
                "Формат:\n"
                "/add ссылка | Название трека"
            )
            return

        url, title = [x.strip() for x in args.split("|", 1)]

        if not url or not title:
            await message.answer("Ссылка и название обязательны.")
            return

        # вытаскиваем id из url
        yandex_track_id = url.rstrip("/").split("/")[-1]

        payload = {
            "url": url,
            "title": title,
            "yandex_track_id": yandex_track_id
        }

        response = requests.post(
            f"{API_URL}/",
            json=payload
        )

        if response.status_code == 200:
            await message.answer("Трек успешно добавлен.")
        else:
            await message.answer(f"Ошибка API:\n{response.text}")

    except Exception as e:
        await message.answer(f"Ошибка:\n{str(e)}")

