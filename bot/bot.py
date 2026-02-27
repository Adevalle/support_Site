import asyncio
import requests
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from config import BOT_TOKEN, API_URL,GET_ADMIN
from state import AddTrack

bot = Bot(BOT_TOKEN)
dpa = Dispatcher()

def is_admin(telegram_id: int) -> bool:
    response = requests.get(GET_ADMIN, params={"telegram_id": telegram_id})
    if response.status_code == 200:
        return True
    else:
        return False

@dpa.message(Command('start'))
async def start(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Ты не админ")
        return
    await message.answer("Привет! Для добавления нового трека отправь команду /add")

@dpa.message(Command("add"))
async def start_add(message: Message, state: FSMContext):
    if not is_admin(message.from_user.id):
        await message.answer("Ты не админ")
        return
    await message.answer("Отправь ссылку на трек:")
    await state.set_state(AddTrack.waiting_for_url)


@dpa.message(AddTrack.waiting_for_url)
async def process_url(message: Message, state: FSMContext):
    await state.update_data(url=message.text.strip())
    await message.answer("Теперь отправь название трека:")
    await state.set_state(AddTrack.waiting_for_title)



@dpa.message(AddTrack.waiting_for_title)
async def process_title(message: Message, state: FSMContext):
    data = await state.get_data()

    payload = {
        "url": data["url"],
        "title": message.text.strip(),
        "added_by": message.from_user.username,
        "telegram_id" : message.from_user.id
    }

    try:
        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            await message.answer("Трек успешно добавлен.")
        else:
            await message.answer(f"Ошибка API: {response.text}, data: {payload}")

    except Exception as e:
        await message.answer(f"Ошибка запроса: {e}")

    await state.clear()


if __name__ == "__main__":
    asyncio.run(dpa.start_polling(bot))


