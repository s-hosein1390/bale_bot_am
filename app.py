from flask import Flask, request
import requests
import os

app = Flask(__name__)

# دریافت توکن از متغیر محیطی (برای امنیت — در Render تنظیم می‌شود)
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("❌ لطفاً متغیر محیطی BOT_TOKEN را در Render تنظیم کنید!")

API_URL = f"https://api.bale.ai/v1/bots/{BOT_TOKEN}/sendMessage"

# متن پیام خوش‌آمدگویی با ایموجی، لینک و فرمت‌بندی Markdown
WELCOME_MESSAGE = """بسم الله الرحمن الرحیم  
به ارتش موعود (عج) خوش آمدی 🌹

🇮🇷 مرحله نخست ثبت‌نام:  
برای ثبت‌نام رسمی فقط کافیه، همراه با مدارک هویتی (کارت ملی و شناسنامه) به محل ثبت‌نام ارتش موعود (عج) مراجعه کنی:

📍 نشانی:  
تهران - خیابان شهید رجائی - بالاتر از بزرگراه آزادگان - مسجد ولی‌الله اعظم عجل‌الله تعالی فرجه‌الشریف  
ساختمان دارالقرآن – طبقه همکف

⸻

📡 مرحله دوم:  
از همین حالا به کانال خبری و آموزشی ارتش موعود (عج) بپیوند تا در جریان آخرین آموزش‌ها، اطلاعیه‌ها و برنامه‌ها قرار بگیری:  
🔗 [قرارگاه موعود (عج)](https://ble.ir/join/HgXmPphmfY)

⸻

🕊️ پشتیبانی و ارتباط با مسئول نیروی انسانی:  
اگر پرسشی، ابهامی یا درخواستی داشتی، می‌تونی مستقیماً با مسئول پشتیبانی در ارتباط باشی:  
👤 [@poshtibaniarteshmowoud](https://ble.ir/poshtibaniarteshmowoud)

یا صاحب‌الزمان ادرکنی. 🤲"""

@app.route('/')
def home():
    """برای بررسی سلامت و فعال نگه داشتن توسط UptimeRobot"""
    return "ربات ارتش موعود (عج) فعال است ✅", 200

@app.route(f'/{BOT_TOKEN}', methods=['POST'])
def webhook():
    """دریافت پیام‌ها از بله و پاسخ به /start"""
    data = request.get_json()
    
    # اگر داده‌ای دریافت نشده یا پیام نباشد، نادیده بگیر
    if not data or 'message' not in data:
        return "OK", 200

    message = data['message']
    chat_id = message['chat']['id']
    text = message.get('text', '')

    # فقط به دستور /start پاسخ بده
    if text == '/start':
        payload = {
            "chat_id": chat_id,
            "text": WELCOME_MESSAGE,
            "parse_mode": "Markdown"  # برای فعال کردن لینک‌ها و فرمت‌بندی
        }
        requests.post(API_URL, json=payload)

    return "OK", 200

if __name__ == '__main__':
    app.run(debug=True)
