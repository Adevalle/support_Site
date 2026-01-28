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
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("meta", property="og:title")
    description_tag = soup.find("meta", property="og:description")
    image_tag = soup.find("meta", property="og:image")

    if not title_tag:
        raise ValueError("Error get name song")

    return {
        "title": title_tag["content"],
        "description": description_tag["content"],
        "cover": image_tag["content"] if image_tag else None
    }