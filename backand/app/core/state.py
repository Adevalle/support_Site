import json
from pathlib import Path

# Абсолютный путь к файлу
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
STATE_FILE = DATA_DIR / "state.json"

def load_state():

    try:
        if STATE_FILE.exists():
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Проверяем наличие ключа
                if "current_track_id" in data:
                    return data
        # Если файл пустой или нет ключа
        return {"current_track_id": "123456"}
    except Exception as e:
        print("Exception load satate:", e)
        return {"current_track_id": "123456"}

def save_state(track_id: str):

    try:
        # Создаём папку, если её нет
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump({"current_track_id": track_id}, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("exception save json:", e)
        raise