import asyncio

import aiohttp
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config import BOT_TOKEN, API_URL,GET_ADMIN
from state import AddTrack

bot = Bot(BOT_TOKEN)
dp = Dispatcher()

def is_admin(telegram_id: int) -> bool:
    response = requests.get(f"{API_URL}/admin/get_admin", params={"telegram_id": telegram_id})
    if response.status_code == 200:
        return True
    else:
        return False

@dp.message(Command('start'))
async def start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Ты не админ")
        return
    await message.answer("Привет! Для добавления нового трека отправь команду /add")

@dp.message(Command("add"))
async def start_add(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Ты не админ")
        return
    await message.answer("Отправь ссылку на трек:")
    await state.set_state(AddTrack.waiting_for_url)


@dp.message(AddTrack.waiting_for_url)
async def process_url(message: Message, state: FSMContext):
    await state.update_data(url=message.text.strip())
    await message.answer("Теперь отправь название трека:")
    await state.set_state(AddTrack.waiting_for_title)



@dp.message(AddTrack.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    data = await state.get_data()

    payload = {
        "url": data["url"],
        "title": message.text.strip(),
        "added_by": message.from_user.username,
        "telegram_id" : message.from_user.id
    }

    try:
        response = requests.post(f"{API_URL}/tracks/current", json=payload)

        if response.status_code == 200:
            await message.answer("Трек успешно добавлен.")
        else:
            await message.answer(f"Ошибка API: {response.text}, data: {payload}")

    except Exception as e:
        await message.answer(f"Ошибка запроса: {e}")

    await state.clear()

@dp.message(Command("history"))
async def history(message: Message):

    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/tracks/history") as resp:

            tracks = await resp.json()

            text = ""

            for t in tracks:
                text += f"{t['id']} — {t['title']}\n"

            await message.answer(text or "История пустая")

@dp.message(Command("delete"))
async def delete_track(message: Message):

    if not is_admin(message.from_user.id):
        await message.answer("Нет прав")
        return

    parts = message.text.split()

    if len(parts) != 2:
        await message.answer("Использование: /delete ID")
        return

    track_id = parts[1]

    async with aiohttp.ClientSession() as session:
        async with session.delete(f"{API_URL}/tracks/delete/{track_id}") as resp:

            if resp.status == 200:
                await message.answer(f"Трек {track_id} удалён")
            else:
                await message.answer("Ошибка удаления")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))


