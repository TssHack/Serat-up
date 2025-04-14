# main.py
import asyncio
import logging
from balethon import Client
from balethon.objects import Message, CallbackQuery # CallbackQuery را هم اضافه کنید چون در dispatcher استفاده می‌شود
# from balethon.conditions import text, callback_data <--- حذف callback_data
from balethon.conditions import text # فقط text را وارد کنید
from config import BOT_TOKEN
import database as db # برای اطمینان از initialize شدن دیتابیس
from handlers.message_handlers import handle_message
from handlers.callback_handlers import on_callback
from handlers.admin_handlers import handle_admin_callbacks

# تنظیمات لاگ‌گیری (اختیاری ولی مفید)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- ربات ---
bot = Client(BOT_TOKEN)

# --- تابع شرطی برای بررسی چت خصوصی ---
def is_private(client: Client, message: Message) -> bool:
    """شرطی برای بررسی اینکه آیا پیام در چت خصوصی ارسال شده است یا خیر"""
    return message.chat.type == "private"

# --- ثبت هندلرها ---
# پیام‌های متنی در چت خصوصی
bot.add_event_handler(handle_message, (text & is_private))

# دکمه‌های اینلاین (عمومی و ادمین)
@bot.on_callback_query()
async def callback_dispatcher(client: Client, query: CallbackQuery):
    """تشخیص و ارسال کال‌بک به هندلر مناسب"""
    # این تابع خودش data را بررسی می‌کند و نیازی به condition ندارد
    data = query.data
    if data.startswith("admin_") or data in ["confirm_broadcast", "cancel_broadcast", "admin_panel"]:
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

