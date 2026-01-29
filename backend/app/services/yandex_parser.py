import re
import requests
from bs4 import BeautifulSoup

TRACK_ID_REGEX = re.compile(r"/track/(\d+)")

def parse_track_id(url: str) -> str:
    match = TRACK_ID_REGEX.search(url)
    if not match:
        raise ValueError("Error get track_id from url")
    return match.group(1)

def fetch_track_metadata(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/121.0.0.0 Safari/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("meta", property="og:title")
    description_tag = soup.find("meta", property="og:description")

    if not title_tag:
        raise print("Error get nsme")

    return {
        "title": title_tag["content"],
        "description": description_tag["content"],
    }