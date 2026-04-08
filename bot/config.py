import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_URL = os.getenv("API_URL")
    GET_ADMIN = os.getenv("GET_ADMIN")
    ADMIN = os.getenv("ADMIN")
