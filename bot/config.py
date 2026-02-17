import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = os.getenv("API_URL")

ADMINS = [int(x) for x in os.getenv("ADMINS").split(",")]