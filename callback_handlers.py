# handlers/callback_handlers.py
import asyncio
from balethon import Client
from balethon.objects import CallbackQuery, Message  # Message برای broadcast
import database as db
import keyboards as kb
import states as st
from utils.helpers import set_user_state, get_user_state, broadcast_message_content
from fonc import ( # توابع خودتان
    get_time, get_hadith, get_fact, get_joke,
    get_fot, get_gold_rate, get_wise_quote, get_zekr
)

async def on_callback(bot: Client, callback_query: CallbackQuery):
    """هندلر دکمه‌های اینلاین"""
    chat_id = callback_query.message.chat.id
    user_id = callback_query.sender.id # ID کاربری که دکمه را زده
    message = callback_query.message # پیام اصلی که دکمه‌ها روی آن هستند
    data = callback_query.data

    # --- دکمه‌های منوی اصلی ---
    if data == "tools":
        await message.edit_text("🔧 **بخش کاربردی و ابزاری**", reply_markup=kb.tools_buttons)
        set_user_state(user_id, st.UserState.NONE)
    elif data == "fun_science":
        await message.edit_text("🎯 **بخش سرگرمی و علمی**", reply_markup=kb.fun_science_buttons)
        set_user_state(user_id, st.UserState.NONE)
    elif data == "ai_services":
        await message.edit_text("🤖 **بخش هوش مصنوعی**", reply_markup=kb.ai_services_buttons)
        set_user_state(user_id, st.UserState.NONE)
    elif data == "return_to_main_menu":
        await message.edit_text("🏠 **منوی اصلی:**", reply_markup=kb.inline_buttons)
        set_user_state(user_id, st.UserState.NONE)
    elif data == "info":
         await message.edit_text(
             "🧑‍💻 این ربات با افتخار توسط **احسان فضلی** و تیم **شفق** توسعه یافته است.\n\n"
             "🔹 ارائه‌دهنده خدمات هوش مصنوعی و ابزارهای کاربردی اسلامی 🔹",
             reply_markup=kb.inline_buttons
         )
         set_user_state(user_id, st.UserState.NONE)
    elif data == "help":
         await message.edit_text(
             "❓ **راهنمای ربات صراط** ❓\n\n"
             "🔹 برای استفاده از امکانات، یکی از گزینه‌های منو را انتخاب کنید.\n"
             "🔹 هر بخش دارای قابلیت‌های منحصربه‌فردی است که می‌توانید از آن بهره ببرید.\n\n"
             "📌 در صورت نیاز به راهنمایی بیشتر، با پشتیبانی در ارتباط باشید.\n"
             "👨‍💻 @Devehsan", # آی‌دی پشتیبانی
             reply_markup=kb.inline_buttons
         )
         set_user_state(user_id, st.UserState.NONE)

    # --- دکمه‌های بخش ابزارها ---
    elif data == "time":
        try:
            time_info = get_time()
            # قالب‌بندی بهبود یافته
            response_text = (
                f"🕰 **زمان دقیق:** {time_info.get('time', 'N/A')}\n"
                f"📆 **تاریخ شمسی:** {time_info.get('shamsi_date', 'N/A')}\n"
                f"🌍 **تاریخ میلادی:** {time_info.get('gregorian_date', 'N/A')}\n"
                f"🌙 **تاریخ قمری:** {time_info.get('hijri_date', 'N/A')}\n"
                f"📅 **روز:** {time_info.get('day', 'N/A')}\n"
                f"🍂 **ماه شمسی:** {time_info.get('month', 'N/A')}\n"
                f"🎯 **روزهای باقی‌مانده تا عید نوروز:** {time_info.get('remaining_days', 'N/A')} روز\n"
                f"✨ **مناسبت روز:** {time_info.get('event', 'بدون مناسبت خاص')}"
            )
            await message.edit_text(response_text, reply_markup=kb.tools_buttons)
        except Exception as e:
            print(f"Error getting time: {e}")
            await message.edit_text("خطا در دریافت اطلاعات زمان.", reply_markup=kb.tools_buttons)
        set_user_state(user_id, st.UserState.NONE)

    elif data == "calculate_age":
        set_user_state(user_id, st.UserState.AWAITING_BIRTHDATE)
        await message.edit_text("🎂 لطفاً تاریخ تولد خود را به صورت YYYY/MM/DD (مثال: 1374/02/04) وارد کنید:", reply_markup=kb.return_to_main_menu_button) # دکمه بازگشت اضافه شد
    elif data == "font":
        set_user_state(user_id, st.UserState.AWAITING_FONT_TEXT)
        await message.edit_text("🧩 متن انگلیسی مورد نظر برای ایجاد فونت را ارسال کنید:", reply_markup=kb.return_to_main_menu_button)
    elif data == "track_parcel":
        set_user_state(user_id, st.UserState.AWAITING_TRACKING_CODE)
        await message.edit_text("📦 لطفاً **کد رهگیری** تیپاکس را ارسال کنید:", reply_markup=kb.return_to_main_menu_button)
    elif data == "w_i": # Weather Info
        set_user_state(user_id, st.UserState.AWAITING_WEATHER_CITY)
        await message.edit_text("🌆 لطفا نام شهر خود را (ترجیحا فارسی) ارسال کنید:", reply_markup=kb.return_to_main_menu_button)
    elif data == "shar": # Shari Times
        set_user_state(user_id, st.UserState.AWAITING_PRAYER_CITY)
        await message.edit_text("🌆 لطفا نام شهر خود را **به انگلیسی** ارسال کنید (مثال: Tehran):", reply_markup=kb.return_to_main_menu_button)
    elif data == "mobi": # Mobile search
        set_user_state(user_id, st.UserState.AWAITING_MOBILE_SEARCH)
        await message.edit_text("**🔎📱 لطفا نام موبایل مورد نظر خود را ارسال کنید:**", reply_markup=kb.return_to_main_menu_button)
    elif data == "mu": # Music search
        set_user_state(user_id, st.UserState.AWAITING_MUSIC_SEARCH)
        await message.edit_text("**🔎🎵 لطفا نام خواننده مورد نظر را ارسال کنید:**", reply_markup=kb.return_to_main_menu_button)
    elif data == "apa": # Aparat search
        set_user_state(user_id, st.UserState.AWAITING_APARAT_SEARCH)
        await message.edit_text("**🔎🎥 موضوع مورد نظر برای جستجو در آپارات را ارسال کنید:**", reply_markup=kb.return_to_main_menu_button)
    elif data == "kala": # Digikala search
        set_user_state(user_id, st.UserState.AWAITING_DIGIKALA_SEARCH)
        await message.edit_text("**🔎💢 نام کالای مورد نظر برای جستجو در دیجی کالا را ارسال کنید:**", reply_markup=kb.return_to_main_menu_button)
    elif data == "fot": # Football today
        try:
            await message.edit_text(get_fot(), reply_markup=kb.tools_buttons)
        except Exception as e:
             print(f"Error getting fot: {e}")
             await message.edit_text("خطا در دریافت اطلاعات بازی‌ها.", reply_markup=kb.tools_buttons)
        set_user_state(user_id, st.UserState.NONE)
    elif data == "gold_rate":
        try:
            await message.edit_text(get_gold_rate(), reply_markup=kb.tools_buttons)
        except Exception as e:
             print(f"Error getting gold rate: {e}")
             await message.edit_text("خطا در دریافت نرخ طلا و سکه.", reply_markup=kb.tools_buttons)
        set_user_state(user_id, st.UserState.NONE)


    # --- دکمه‌های بخش سرگرمی و علمی ---
    elif data == "hadith":
        try:
            hadith, speaker = get_hadith()
            await message.edit_text(f"📖 **حدیث:**\n{hadith}\n\n🗣️ **{speaker}**", reply_markup=kb.fun_science_buttons)
        except Exception as e:
             print(f"Error getting hadith: {e}")
             await message.edit_text("خطا در دریافت حدیث.", reply_markup=kb.fun_science_buttons)
        set_user_state(user_id, st.UserState.NONE)
    elif data == "fact":
        try:
            fact, source = get_fact()
            await message.edit_text(f"📌 **دانستنی:**\n{fact}\n\n✏️ **موضوع:** ({source})", reply_markup=kb.fun_science_buttons)
        except Exception as e:
             print(f"Error getting fact: {e}")
             await message.edit_text("خطا در دریافت دانستنی.", reply_markup=kb.fun_science_buttons)
        set_user_state(user_id, st.UserState.NONE)
    elif data == "random_joke":
        try:
            await message.edit_text(get_joke(), reply_markup=kb.fun_science_buttons)
        except Exception as e:
             print(f"Error getting joke: {e}")
             await message.edit_text("خطا در دریافت جوک.", reply_markup=kb.fun_science_buttons)
        set_user_state(user_id, st.UserState.NONE)
    elif data == "so": # Sokhan Bozorgan
        try:
            await message.edit_text(get_wise_quote(), reply_markup=kb.fun_science_buttons)
        except Exception as e:
             print(f"Error getting quote: {e}")
             await message.edit_text("خطا در دریافت سخن بزرگان.", reply_markup=kb.fun_science_buttons)
        set_user_state(user_id, st.UserState.NONE)
    elif data == "zekr":
        try:
            await message.edit_text(get_zekr(), reply_markup=kb.fun_science_buttons)
        except Exception as e:
             print(f"Error getting zekr: {e}")
             await message.edit_text("خطا در دریافت ذکر هفته.", reply_markup=kb.fun_science_buttons)
        set_user_state(user_id, st.UserState.NONE)


    # --- دکمه‌های بخش هوش مصنوعی ---
    elif data == "ai_chat": # دستیار مومن
        set_user_state(user_id, st.UserState.CHATTING_AI_ASSISTANT)
        await message.edit_text("🤖 **پیام خود را برای دستیار مومن ارسال کنید:**\n(برای خروج و بازگشت، دکمه زیر را بزنید)", reply_markup=kb.Ai_back_button)
    elif data == "gpt": # ChatGPT-4o
        set_user_state(user_id, st.UserState.CHATTING_GPT4)
        await message.edit_text("🧩 **پیام خود را برای ChatGPT-4o بفرستید:**\n(برای خروج و بازگشت، دکمه زیر را بزنید)", reply_markup=kb.Ai_back_button)
    elif data == "gpt1": # هوش مصنوعی حافظه دار
        set_user_state(user_id, st.UserState.CHATTING_GPT1)
        await message.edit_text("🧠 **پیام خود را برای هوش مصنوعی حافظه‌دار بفرستید:**\n(برای خروج و بازگشت، دکمه زیر را بزنید)", reply_markup=kb.Ai_back_button)
    elif data == "translate":
        set_user_state(user_id, st.UserState.AWAITING_TRANSLATION_TEXT)
        await message.edit_text("📜 **متن انگلیسی مورد نظر برای ترجمه به فارسی را ارسال کنید:**", reply_markup=kb.return_to_main_menu_button) # بازگشت به منو اصلی مناسب‌تر است
    elif data == "lawyer":
        set_user_state(user_id, st.UserState.CHATTING_LAWYER)
        await message.edit_text("⚖️ **سوال حقوقی خود را از وکیل هوش مصنوعی بپرسید:**\n(برای خروج و بازگشت، دکمه زیر را بزنید)", reply_markup=kb.Ai_back_button)
    elif data == "psychologist":
        set_user_state(user_id, st.UserState.CHATTING_PSYCHOLOGIST)
        await message.edit_text("🧠 **موضوع مورد نظر برای مشاوره با روانشناس هوش مصنوعی را مطرح کنید:**\n(برای خروج و بازگشت، دکمه زیر را بزنید)", reply_markup=kb.Ai_back_button)
    # دکمه Ai_b (بازگشت به منوی AI) در کد قبلی شما بود، اینجا همسان‌سازی شد با ai_services
    # elif data == "Ai_b":
    #     await message.edit_text("🤖 **بخش هوش مصنوعی**", reply_markup=kb.ai_services_buttons)
    #     set_user_state(user_id, st.UserState.NONE)

    # --- دکمه‌های پنل ادمین ---
    elif data == "admin_panel":
        if db.is_user_admin(user_id):
             await message.edit_text("👑 **پنل مدیریت ربات** 👑", reply_markup=kb.admin_panel_buttons)
        else:
             await callback_query.answer("🚫 دسترسی غیرمجاز", show_alert=True) # نمایش پیام خطا به کاربر
        # وضعیت کاربر تغییر نمی‌کند

    # --- پاسخ به callback query (اختیاری ولی خوب است) ---
    try:
        # اگر عملیات زمان‌بر نیست، سریع پاسخ دهید
        if data not in ["admin_panel"]: # مثال: برای پنل ادمین که فقط متن را ویرایش می‌کند نیازی نیست
             await callback_query.answer()
    except Exception as e:
        print(f"Error answering callback query {callback_query.id}: {e}")
