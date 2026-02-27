import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

ADMINS = [123456789]  # вставь свой telegram id

API_URL = "http://127.0.0.1:8000/api/tracks"