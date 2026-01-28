import requests
from bs4 import BeautifulSoup
import time

# ========= Telegram =========
BOT_TOKEN = "你的_BOT_TOKEN"
CHAT_ID = "你的_CHAT_ID"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "HTML"
    }
    requests.post(url, data=payload, timeout=10)

# ========= 商品列表 =========
PRODUCTS = {
    "Astrox 100ZZ Dark Navy": "https://vsmash.com/product/yonex-astrox-100zz-dark-navy",
    "Astrox 100VA ZZ Grayish Beige": "https://vsmash.com/product/yonex-astrox-100va-zz-grayish-beige",
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

already_notified = set()

def check_stock(name, url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    buttons = soup.find_all("button")
    for btn in buttons:
        if "add to bag" in btn.get_text(strip=True).lower():
            return True
    return False

# ========= 主循环 =========
while True:
    for name, url in PRODUCTS.items():
        if name in already_notified:
            continue

        try:
            if check_stock(name, url):
                msg = f"🔥 <b>{name}</b> 补货了！\n\n👉 {url}"
                send_telegram(msg)
                already_notified.add(name)
        except Exception as e:
            print("Error:", e)

    time.sleep(300)  # 每 5 分钟检查
