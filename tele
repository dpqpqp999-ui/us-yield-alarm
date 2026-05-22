import requests
from datetime import datetime

import os
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
FRED_API_KEY = os.environ["FRED_API_KEY"]

def get_yield(series_id):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 2
    }
    res = requests.get(url, params=params)
    data = res.json()["observations"]
    today_val = float(data[0]["value"])
    prev_val = float(data[1]["value"])
    change = today_val - prev_val
    return today_val, change

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML"})

def main():
    y10, c10 = get_yield("DGS10")
    y30, c30 = get_yield("DGS30")

    arrow10 = "🔺" if c10 > 0 else "🔻" if c10 < 0 else "➡️"
    arrow30 = "🔺" if c30 > 0 else "🔻" if c30 < 0 else "➡️"

    msg = f"""📊 <b>미국 국채 금리 알림</b>
{datetime.now().strftime('%Y-%m-%d')} 08:30

<b>10년물</b>: {y10:.3f}%  {arrow10} ({c10:+.3f}%)
<b>30년물</b>: {y30:.3f}%  {arrow30} ({c30:+.3f}%)

🔗 출처: FRED (연준 공식 데이터)"""

    send_telegram(msg)

if __name__ == "__main__":
    main()
