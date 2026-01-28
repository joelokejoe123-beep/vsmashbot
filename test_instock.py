import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")      # Render / 本机环境变量
CHAT_ID = os.getenv("CHAT_ID")

URL = "https://vsmash.com/product/yonex-astrox-100zz-kurenai"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data, timeout=10)

def test_stock():
    r = requests.get(URL, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    for btn in soup.find_all("button"):
        if "add to bag" in btn.get_text(strip=True).lower():
            return True
    return False


if test_stock():
    send_telegram("✅【TEST 成功】\nAstrox 100ZZ Kurenai 目前是【有货】")
    print("TEST OK – 有货")
else:
    print("TEST FAIL – 没抓到 Add to bag")
