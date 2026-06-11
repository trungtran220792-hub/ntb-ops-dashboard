import sys
sys.path.append('.')
import requests
import os
import json
from dotenv import load_dotenv
from app import app, get_overall_metrics_summary, load_config

load_dotenv()
config = load_config()
bot_token = config.get("telegram_bot_token", "").strip()
chat_id = config.get("telegram_chat_id", "").strip()
gemini_api_key = config.get("gemini_api_key", "").strip()

print("Restored Gemini Key (masked):", gemini_api_key[:10] + "..." if gemini_api_key else "None")
print("Telegram Bot Token (masked):", bot_token[:10] + "..." if bot_token else "None")
print("Telegram Chat ID:", chat_id)

with app.app_context():
    try:
        summary = get_overall_metrics_summary()
        print("Summary loaded successfully.")
        
        worst_gtc_str = ", ".join([f"{item['name']} ({item['province']}): {item['pct']:.1f}% GTC" for item in summary['worst_gtc']])
        worst_ltc_str = ", ".join([f"{item['name']} ({item['province']}): {item['pct']:.1f}% LTC" for item in summary['worst_ltc']])
        
        if summary['spikes']:
            spikes_str = "\n".join([f"- {s['name']} ({s['province']}): +{s['growth_abs']:,} đơn (+{s['growth_pct']}%)" for s in summary['spikes']])
        else:
            spikes_str = "Không phát hiện bưu cục tăng đơn đột biến."
            
        prompt = (
            f"Bạn là một AI Trợ lý Vận hành cao cấp phụ trách Vùng NTB của hệ thống Giao Hàng Nhanh (GHN).\n"
            f"Hãy phân tích dữ liệu vận hành tổng thể ngày {summary['date']} dưới đây và viết một bản tin phân tích cảnh báo đầu ngày gửi cho Group Telegram của Ban điều hành.\n\n"
            f"Dữ liệu vận hành ngày {summary['date']}:\n"
            f"1. Các chỉ số chính (KPI) hôm nay:\n"
            f"   - Giao thành công (% GTC): {summary['today']['gtc_pct']}%\n"
            f"   - Lưu kho thành công (% LTC): {summary['today']['ltc_pct']}%\n"
            f"   - Tổng sản lượng GTC: {summary['today']['gtc_vol']:,} đơn\n"
            f"   - Tổng sản lượng LTC: {summary['today']['ltc_vol']:,} đơn\n\n"
            f"2. So sánh hiệu suất (Tỷ lệ tăng/giảm %):\n"
            f"   - So với 3 ngày trước:\n"
            f"     + GTC: {round(summary['today']['gtc_pct'] - (summary['n3']['gtc_pct'] if summary['n3'] else 0), 2):+}% \n"
            f"     + LTC: {round(summary['today']['ltc_pct'] - (summary['n3']['ltc_pct'] if summary['n3'] else 0), 2):+}% \n"
            f"   - So với tuần trước:\n"
            f"     + GTC: {round(summary['today']['gtc_pct'] - (summary['lw']['gtc_pct'] if summary['lw'] else 0), 2):+}% \n"
            f"     + LTC: {round(summary['today']['ltc_pct'] - (summary['lw']['ltc_pct'] if summary['lw'] else 0), 2):+}% \n\n"
            f"3. Đơn tồn đọng (Backlog):\n"
            f"   - Tổng tồn đọng: {summary['backlog']['total']:,} đơn\n"
            f"     + Chưa giao (Aging): {summary['backlog']['chua_giao']:,} đơn\n"
            f"     + Chưa lấy (Treo giao): {summary['backlog']['chua_lay']:,} đơn\n"
            f"     + Chưa trả (Treo trả): {summary['backlog']['chua_tra']:,} đơn\n\n"
            f"4. Bưu cục cần đặc biệt lưu ý hôm nay (Hiệu suất tệ nhất):\n"
            f"   - Top GTC thấp nhất: {worst_gtc_str}\n"
            f"   - Top LTC thấp nhất: {worst_ltc_str}\n\n"
            f"5. Cảnh báo sản lượng tạo đơn tăng đột biến:\n"
            f"   {spikes_str}\n\n"
            f"Yêu cầu định dạng bản tin gửi Telegram:\n"
            f"- Định dạng Markdown chuẩn của Telegram (sử dụng *chữ đậm*, `chữ code`, biểu tượng emoji thích hợp).\n"
            f"- Tránh sử dụng các ký tự đặc biệt làm lỗi bộ phân tích cú pháp Markdown của Telegram (như dấu ngoặc vuông hoặc dấu gạch dưới đơn lẻ không đóng cặp). Hãy giữ Markdown đơn giản bằng cách dùng dấu * cho chữ đậm và không lồng ghép định dạng.\n"
            f"- Phong cách viết: Chuyên nghiệp, nghiêm túc, tập trung vào hành động nhanh và chỉ rõ các điểm nóng cần khắc phục (đặc biệt lưu ý bưu cục hiệu suất thấp hoặc có sản lượng tăng đột biến).\n"
            f"- Hãy chia rõ 4 phần sau:\n"
            f"  * 📊 *BẢN TIN VẬN HÀNH ĐẦU NGÀY VÙNG NTB* ({summary['date']})\n"
            f"  * ⚠️ *CẢNH BÁO ĐIỂM NÓNG* (Bưu cục yếu kém và backlog cao)\n"
            f"  * 🚨 *CẢNH BÁO SẢN LƯỢNG ĐỘT BIẾN*\n"
            f"  * 💡 *HÀNH ĐỘNG KHUYẾN NGHỊ* (Gợi ý hành động thực tế cho AM và Bưu cục trưởng)"
        )
        
        # Call Gemini REST API
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={gemini_api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        print("Calling Gemini API...")
        res_gemini = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=30)
        print("Gemini Status Code:", res_gemini.status_code)
        
        if res_gemini.status_code == 200:
            gemini_data = res_gemini.json()
            message = gemini_data['candidates'][0]['content']['parts'][0]['text']
            print("Gemini generated response successfully.")
        else:
            print("Gemini error details:", res_gemini.text)
            sys.exit(1)
            
        # Send message to Telegram
        url_tele = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload_tele = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "Markdown"
        }
        print("Sending message to Telegram...")
        res_tele = requests.post(url_tele, json=payload_tele, timeout=10)
        print("Telegram Status Code:", res_tele.status_code)
        
        if res_tele.status_code != 200:
            print("Telegram failed, fallback to plain text...")
            payload_tele["parse_mode"] = ""
            res_tele_plain = requests.post(url_tele, json=payload_tele, timeout=10)
            print("Fallback status:", res_tele_plain.status_code)
            print("Fallback text:", res_tele_plain.text)
        else:
            print("Sent successfully to Telegram!")
            print("Response:", res_tele.text)
            
    except Exception as e:
        print("Exception occurred:")
        import traceback
        traceback.print_exc()
