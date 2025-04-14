# main.py
import asyncio
import logging
from balethon import Client
from balethon.objects import Message, CallbackQuery
from balethon.conditions import text
from config import BOT_TOKEN
import database as db
from message_handlers import handle_message
from callback_handlers import on_callback
from admin_handlers import handle_admin_callbacks

# تنظیمات لاگ‌گیری
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- ربات ---
bot = Client(BOT_TOKEN)

# --- تابع شرطی برای بررسی چت خصوصی ---
def is_private(client: Client, message: Message) -> bool:
    return message.chat.type == "private"

# --- ثبت هندلرها ---
bot.add_event_handler(handle_message, (text & is_private))

# --- تغییر در تعریف callback_dispatcher ---
@bot.on_callback_query()
async def callback_dispatcher(client: Client, *args): # دریافت آرگومان‌ها با *args
    """
    تشخیص و ارسال کال‌بک به هندلر مناسب.
    از *args برای سازگاری بیشتر با نحوه ارسال آرگومان‌ها استفاده می‌شود.
    """
    print(f"DEBUG: callback_dispatcher called with args: {args}") # برای خطایابی

    if not args:
        logger.error("callback_dispatcher received no arguments in *args!")
        return
    
    # فرض می‌کنیم اولین آرگومان بعد از client همان query object است
    query = args[0] 

    # بررسی می‌کنیم که آیا واقعا CallbackQuery است یا نه
    if not isinstance(query, CallbackQuery):
        logger.error(f"callback_dispatcher expected CallbackQuery but received {type(query)}")
        # شاید بخواهید آپدیت‌های غیرمنتظره را نادیده بگیرید
        # return 
        # یا اگر می‌خواهید خطا را ببینید، می‌توانید آن را raise کنید
        raise TypeError(f"Expected CallbackQuery, got {type(query)}")


    # بقیه کد مثل قبل
    data = query.data
    logger.info(f"Callback query received: Data='{data}', User={query.sender.id}, Chat={query.message.chat.id if query.message else 'N/A'}")

    try:
        if data.startswith("admin_") or data in ["confirm_broadcast", "cancel_broadcast", "admin_panel"]:
            await handle_admin_callbacks(client, query)
        else:
            await on_callback(client, query) # هندلر عمومی
    except Exception as e:
        # لاگ کردن خطاهایی که ممکن است در هندلرهای on_callback یا handle_admin_callbacks رخ دهد
        logger.error(f"Error processing callback data '{data}': {e}", exc_info=True)
        try:
            # اطلاع به کاربر در صورت امکان
            await query.answer("خطایی در پردازش درخواست شما رخ داد!", show_alert=True)
        except Exception as answer_err:
             logger.error(f"Could not send error answer for callback query: {answer_err}")


# --- اجرای ربات ---
if __name__ == "__main__":
    print("Initializing Database...")
    db.initialize_database()
    print("Starting Bot...")
    try:
        bot.run()
    except Exception as e:
        logger.error(f"Bot crashed: {e}", exc_info=True)
    finally:
        print("Bot stopped.")

