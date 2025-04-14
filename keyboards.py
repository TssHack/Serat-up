# keyboards.py
from balethon.objects import InlineKeyboard, InlineKeyboardButton, ReplyKeyboard # ReplyKeyboard اگر نیاز دارید
# from config import CHANNEL_USERNAME # اگر لینک کانال پویاست

# --- کیبوردهای اصلی ---
inline_buttons = InlineKeyboard(
    [("🤖 بخش هوش مصنوعی", "ai_services")],
    [("📌 بخش کاربردی و ابزاری", "tools")],
    [("🎯 بخش سرگرمی و علمی", "fun_science")],
    [("ℹ️ درباره ما", "info"), ("راهنما 🧬", "help")],
    [("👑 پنل ادمین", "admin_panel")] # دکمه پنل ادمین
)

tools_buttons = InlineKeyboard(
    [("اعلام زمان ⏰", "time"), ("اوقات شرعی 🌆", "shar")],
    [("فونت ساز 🦄", "font"), ("محاسبه سن 🎂", "calculate_age")],
    [("دریافت نرخ طلا و سکه 💰", "gold_rate"), ("وضعیت آب و هوا ⛅️", "w_i")],
    [("بازی های امروز ⚽️", "fot"), ("پیگیری مرسوله تیپاکس 📦", "track_parcel")],
    [("جستجوی گوشی 📱", "mobi"), ("جستجو در آپارات 🎥", "apa")],
    [("جستجو در دیجی کالا 🗣️", "kala"), ("جستجو خواننده 🎵", "mu")],
    [("بازگشت به منو اصلی 🏠", "return_to_main_menu")]
)

fun_science_buttons = InlineKeyboard(
    [("حدیث 📖", "hadith"), ("جوک تصادفی 😂", "random_joke")],
    [("دانستنی 🧠", "fact"), ("سخن بزرگان 🗣️", "so")],
    [("ذکر هفته 📿", "zekr")],
    [("بازگشت به منو اصلی 🏠", "return_to_main_menu")]
)

ai_services_buttons = InlineKeyboard(
    [("هوش مصنوعی حافظه دار 🧠", "gpt1")],
    [("دستیار مومن 🤖", "ai_chat")],
    [("وکیل ⚖️", "lawyer"), ("روانشناس 🧠", "psychologist")],
    [("ChatGPT-4o 🧩", "gpt")],
    [("مترجم انگلیسی 📝", "translate")],
    [("بازگشت به منو اصلی 🏠", "return_to_main_menu")]
)

return_to_main_menu_button = InlineKeyboard([("بازگشت به منو اصلی 🏠", "return_to_main_menu")])

# --- کیبوردهای مخصوص AI ---
Ai_back_button = InlineKeyboard([("🔙 بازگشت به بخش هوش مصنوعی", "ai_services")]) # بهبود نام

# --- کیبوردهای ادمین ---
admin_panel_buttons = InlineKeyboard(
    [("📊 آمار ربات", "admin_stats"), ("📢 ارسال همگانی", "admin_broadcast")],
    [("➕ افزودن ادمین", "admin_add"), ("➖ حذف ادمین", "admin_remove")],
    # [("🚫 مدیریت کاربران بن شده", "admin_ban_list")], # در صورت پیاده‌سازی بن
    [("بازگشت به منو اصلی 🏠", "return_to_main_menu")]
)

confirm_broadcast_buttons = InlineKeyboard(
    [("✅ بله، ارسال کن", "confirm_broadcast"), ("❌ لغو", "cancel_broadcast")]
)

# کیبورد عضویت در کانال (اگر نیاز دارید)
# join_channel_keyboard = InlineKeyboard([
#     [InlineKeyboardButton(text="📢 عضویت در کانال", url=f"https://ble.ir/{CHANNEL_USERNAME.lstrip('@')}")],
#     [InlineKeyboardButton(text="✅ بررسی عضویت", callback_data="check_subscription")]
# ])
