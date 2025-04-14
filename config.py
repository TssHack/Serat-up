# config.py
import os
from dotenv import load_dotenv

load_dotenv() # Loads variables from .env file if it exists

BOT_TOKEN = os.getenv("BOT_TOKEN", "1752263879:AR7EWOyRTpIcTXyQG7kq3ZbHFBaAyFV43rEC8krO") # توکن ربات خود را اینجا یا در فایل .env قرار دهید
ADMIN_USER_IDS = [int(admin_id) for admin_id in os.getenv("ADMIN_USER_IDS", "2143480267").split(',')] # لیست ایدی عددی ادمین‌ها (جدا شده با کاما)
# مثال: ADMIN_USER_IDS = "12345678,98765432"

DATABASE_NAME = "bot_database.db"
CHANNEL_USERNAME = "@shafag_tm" # نام کاربری کانال با @ یا بدون آن
# CHANNEL_ID = -1001234567890 # اگر از ID عددی استفاده می‌کنید
