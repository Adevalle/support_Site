import requests
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from config import BOT_TOKEN, API_URL, ADMINS

bot = Bot(BOT_TOKEN)
dp = Dispatcher()


def is_admin(user_id):
    return user_id in ADMINS


@dp.message(Command("start"))
async def start(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("Нет доступа.")
        return

    await message.answer(
        "Поддержка.fm бот\n\n"
        "Добавление трека:\n"
        "/add ссылка | название"
    )


@dp.message(Command("add"))
async def add_track(message: types.Message):
    if not is_admin(message.from_user.id):
        return

    args = message.text.replace("/add", "").strip()

    if "|" in args:
        url, title = [x.strip() for x in args.split("|", 1)]
    else:
        url , title = args, None


    payload = {
        "url": url,
        "title": title
    }

    try:
        r = requests.post(API_URL, json=payload, timeout=10)

        if r.status_code == 200:
            await message.answer("Трек добавлен.")
        else:
            await message.answer(f"Ошибка API:\n{r.text}")

    except Exception as e:
        await message.answer(f"Ошибка: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))
