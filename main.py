# main.py
import asyncio
import logging
from balethon import Client
from balethon.conditions import text, private_chat, callback_data # یا سایر conditions مورد نیاز
from config import BOT_TOKEN
import database as db # برای اطمینان از initialize شدن دیتابیس
from handlers.message_handlers import handle_message
from handlers.callback_handlers import on_callback
from handlers.admin_handlers import handle_admin_callbacks # هندلر جدید ادمین

# تنظیمات لاگ‌گیری (اختیاری ولی مفید)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- ربات ---
bot = Client(BOT_TOKEN)

# --- ثبت هندلرها ---
# پیام‌های متنی در چت خصوصی
bot.add_event_handler(handle_message, (text & private_chat))

# دکمه‌های اینلاین (عمومی و ادمین)
# تفکیک هندلر کال‌بک‌ها برای خوانایی بهتر
@bot.on_callback_query()
async def callback_dispatcher(client: Client, query: CallbackQuery):
    """تشخیص و ارسال کال‌بک به هندلر مناسب"""
    data = query.data
    if data.startswith("admin_") or data in ["confirm_broadcast", "cancel_broadcast"]:
        await handle_admin_callbacks(client, query)
    else:
        await on_callback(client, query) # هندلر عمومی

# --- اجرای ربات ---
if __name__ == "__main__":
    print("Initializing Database...")
    db.initialize_database() # اطمینان مجدد از ساخت جداول
    print("Starting Bot...")
    try:
        bot.run()
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
    finally:
        print("Bot stopped.")

