import sys
sys.path.append('.')
import requests
import os
from dotenv import load_dotenv
from app import app, get_spiking_post_offices, load_config

load_dotenv()
config = load_config()
bot_token = config.get("telegram_bot_token", "").strip()
chat_id = config.get("telegram_chat_id", "").strip()

print("Telegram Bot Token (masked):", bot_token[:10] + "..." if bot_token else "None")
print("Telegram Chat ID:", chat_id)

with app.app_context():
    try:
        spikes = get_spiking_post_offices()
        print("Spikes count:", len(spikes))
        if spikes:
            items_str = ""
            for idx, item in enumerate(spikes):
                items_str += f"{idx + 1}. *{item['name']}* ({item['province']})\n"
                items_str += f"   - Sản lượng hôm nay: *{item['value']:,}* đơn\n"
                items_str += f"   - Tăng trưởng 7D: *+{item['growth_abs']:,}* đơn (*+{item['growth_pct']}%*)\n\n"
                
            message = (
                f"🚨 *CẢNH BÁO SẢN LƯỢNG TẠO ĐƠN TĂNG ĐỘT BIẾN* 🚨\n"
                f"(So sánh sản lượng hôm nay với 7 ngày trước)\n\n"
                f"Danh sách bưu cục có sản lượng tăng đột biến (>30% và >50 đơn):\n\n"
                f"{items_str}"
                f"📊 *Tổng quan:* Phát hiện {len(spikes)} bưu cục tăng đột biến trong Vùng."
            )
        else:
            message = (
                f"ℹ️ *BÁO CÁO SẢN LƯỢNG TẠO ĐƠN VÙNG* ℹ️\n"
                f"Không phát hiện bưu cục nào có sản lượng tăng đột biến (>30% và >50 đơn) trong 7 ngày qua."
            )
            
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        res = requests.post(url, json=payload, timeout=10)
        print("Telegram Response Status:", res.status_code)
        print("Telegram Response Text:", res.text)
    except Exception as e:
        print("Exception occurred:")
        import traceback
        traceback.print_exc()
