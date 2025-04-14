# main.py
import asyncio
import logging
from balethon import Client
from balethon.objects import Message # Message را برای تابع شرطی نیاز داریم
# from balethon.conditions import text, private_chat, callback_data <--- حذف private_chat
from balethon.conditions import text, callback_data # فقط text و callback_data را وارد کنید
from config import BOT_TOKEN
import database as db # برای اطمینان از initialize شدن دیتابیس
from message_handlers import handle_message
from callback_handlers import on_callback
from admin_handlers import handle_admin_callbacks # هندلر جدید ادمین

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
# از ترکیب text و تابع is_private استفاده کنید
bot.add_event_handler(handle_message, (text & is_private))

# دکمه‌های اینلاین (عمومی و ادمین)
# تفکیک هندلر کال‌بک‌ها برای خوانایی بهتر
# (توجه: در بالتون معمولاً @bot.on_callback_query() کافی است و خودش تفکیک را انجام می‌دهد)
# اما اگر می‌خواهید مانند کد قبلی باشد، می‌توانید dispatcher را نگه دارید:
@bot.on_callback_query()
async def callback_dispatcher(client: Client, query: CallbackQuery):
    """تشخیص و ارسال کال‌بک به هندلر مناسب"""
    data = query.data
    # بهتر است بررسی دسترسی ادمین را داخل خود هندلر ادمین انجام دهیم
    # if data.startswith("admin_") or data in ["confirm_broadcast", "cancel_broadcast"]:
    #     await handle_admin_callbacks(client, query)
    # else:
    #     await on_callback(client, query) # هندلر عمومی

    # روش ساده‌تر: همه کال‌بک‌ها به یک هندلر می‌روند و آنجا تفکیک می‌شوند
    # یا می‌توانید دو هندلر جدا با conditions ثبت کنید:
    # bot.add_event_handler(handle_admin_callbacks, callback_data.startswith("admin_") | callback_data == "confirm_broadcast" | callback_data == "cancel_broadcast")
    # bot.add_event_handler(on_callback, ~callback_data.startswith("admin_") & callback_data != "confirm_broadcast" & callback_data != "cancel_broadcast")

    # فعلا همان dispatcher قبلی را نگه می‌داریم، اما بررسی ادمین را به داخل تابع منتقل می‌کنیم
    if data.startswith("admin_") or data in ["confirm_broadcast", "cancel_broadcast", "admin_panel"]: # admin_panel هم مربوط به ادمین است
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

