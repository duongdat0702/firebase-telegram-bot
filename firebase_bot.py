import firebase_admin
from firebase_admin import credentials, db
import requests
import time
import os, json

# Thông tin bot Telegram
BOT_TOKEN = '7847098252:AAGDc69rCFe8F1_2cBHjwuwRdnMSnq3XAf8'  # Thay bằng BOT_TOKEN của bạn
CHAT_ID = '-4723792950'  # ID của bạn hoặc nhóm
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

# Khởi tạo Firebase
firebase_json = os.environ['FIREBASE_CREDENTIALS_JSON']
cred_dict = json.loads(firebase_json)
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://duan1-497fe-default-rtdb.firebaseio.com/'
})

# Hàm gửi tin nhắn Telegram
def send_telegram(message):
    payload = {
        'chat_id': CHAT_ID,
        'text': message
    }
    r = requests.post(TELEGRAM_API, data=payload)
    print("Telegram status:", r.status_code)

# Theo dõi thay đổi trên Firebase
def main():
    ref = db.reference('/Alert/Message')
    last_msg = None

    while True:
        try:
            msg = ref.get()
            if msg and msg != last_msg:
                print("🔥 Tin nhắn mới từ Firebase:", msg)
                send_telegram(msg)
                last_msg = msg
        except Exception as e:
            print("Lỗi:", e)

        time.sleep(2)  # Kiểm tra mỗi 2 giây

if __name__ == '__main__':
    main()
