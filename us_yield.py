import requests
from datetime import datetime
import os

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

def get_yield(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"interval": "1d", "range": "5d"}
    res = requests.get(url, headers=headers, params=params)
    data = res.json()["chart"]["result"][0]
    closes = data["indicators"]["quote"][0]["close"]
    closes = [x for x in closes if x is not None]
    today = closes[-1]
    prev = closes[-2]
    change = today - prev
    return today, change

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"})

def main():
    y10, c10 = get_yield("^TNX")   # 10년물
    y30, c30 = get_yield("^TYX")   # 30년물

    arrow10 = "🔺" if c10 > 0 else "🔻" if c10 < 0 else "➡️"
    arrow30 = "🔺" if c30 > 0 else "🔻" if c30 < 0 else "➡️"

    msg = f"""📊 <b>미국 국채 금리 알림</b>
{datetime.now().strftime('%Y-%m-%d')} 08:30

<b>10년물</b>: {y10:.3f}%  {arrow10} ({c10:+.3f}%)
<b>30년물</b>: {y30:.3f}%  {arrow30} ({c30:+.3f}%)

🔗 출처: Yahoo Finance"""

    send_telegram(msg)

if __name__ == "__main__":
    main()
