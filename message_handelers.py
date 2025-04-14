# handlers/message_handlers.py
from balethon import Client
from balethon.objects import Message
import database as db
import keyboards as kb
import states as st
from utils.helpers import get_user_state, set_user_state, send_typing_action, format_user_info
from fonc import ( # وارد کردن توابع خودتان
    get_prayer_times, chat_with_ai_api, chat_with_ai, chat_with_lawyer,
    chat_with_psychologist, get_gpt, get_translate, convert_to_fonts,
    calculate_age, track_parcel, mobile, aparat, digikala, music
)
from config import ADMIN_USER_IDS # برای تنظیم اولیه ادمین‌ها

async def handle_message(bot: Client, message: Message):
    """هندلر اصلی پیام‌ها"""
    user = message.from_user
    chat_id = message.chat.id

    # ثبت یا آپدیت کاربر در دیتابیس
    db.add_or_update_user(user.id, user.first_name, user.last_name, user.username)

    # بررسی دستور /start
    if message.text and message.text.lower() == "/start":
        set_user_state(chat_id, st.UserState.NONE) # ریست کردن وضعیت
        # بررسی و تنظیم ادمین اولیه (اگر کاربر در لیست کانفیگ باشد)
        if user.id in ADMIN_USER_IDS and not db.is_user_admin(user.id):
             db.set_admin_status(user.id, True)
             await message.reply("✅ شما به عنوان ادمین اولیه تنظیم شدید.")

        await message.reply(
             f"🤖 سلام {user.first_name}! به ربات صراط خوش آمدید!\n\n"
             "✨ دستیار هوشمند اسلامی شما ✨\n\n"
             "📌 این ربات امکانات متنوعی را در اختیار شما قرار می‌دهد:",
             reply_markup=kb.inline_buttons
        )
        return # پایان پردازش برای /start

    # بررسی دستور /admin (فقط برای ادمین‌ها)
    if message.text and message.text.lower() == "/admin":
        if db.is_user_admin(chat_id):
            await message.reply("👑 **پنل مدیریت ربات** 👑\n\nلطفا یک گزینه را انتخاب کنید:", reply_markup=kb.admin_panel_buttons)
        else:
            await message.reply("🚫 شما دسترسی به این بخش را ندارید.")
        return

    # دریافت وضعیت فعلی کاربر
    current_state = get_user_state(chat_id)

    # --- پردازش پیام‌ها بر اساس وضعیت ---

    if current_state == st.UserState.AWAITING_TRACKING_CODE:
        await send_typing_action(bot, chat_id)
        tracking_code = message.text.strip()
        try:
            response = track_parcel(tracking_code) # فرض می‌کنیم این تابع خطاها را مدیریت می‌کند
            await message.reply(response, reply_markup=kb.tools_buttons)
        except Exception as e:
            print(f"Error tracking parcel: {e}")
            await message.reply("خطایی در پیگیری مرسوله رخ داد. لطفا دوباره تلاش کنید.", reply_markup=kb.tools_buttons)
        set_user_state(chat_id, st.UserState.NONE)

    elif current_state == st.UserState.AWAITING_PRAYER_CITY:
        await send_typing_action(bot, chat_id)
        city = message.text.strip()
        try:
            response = get_prayer_times(city)
            await message.reply(response, reply_markup=kb.tools_buttons)
        except Exception as e:
            print(f"Error getting prayer times for {city}: {e}")
            await message.reply(f"خطا در دریافت اوقات شرعی شهر '{city}'. مطمئن شوید نام شهر را به انگلیسی صحیح وارد کرده‌اید.", reply_markup=kb.tools_buttons)
        set_user_state(chat_id, st.UserState.NONE)

    elif current_state == st.UserState.AWAITING_FONT_TEXT:
        await send_typing_action(bot, chat_id)
        text = message.text.strip()
        try:
            response = convert_to_fonts(text)
            await message.reply(response, reply_markup=kb.tools_buttons)
        except Exception as e:
            print(f"Error converting font: {e}")
            await message.reply("خطایی در ساخت فونت رخ داد.", reply_markup=kb.tools_buttons)
        set_user_state(chat_id, st.UserState.NONE)

    elif current_state == st.UserState.AWAITING_WEATHER_CITY:
        await send_typing_action(bot, chat_id)
        city = message.text.strip()
        try:
            response = get_weather(city) # فرض می‌کنیم تابع شما وجود دارد
            await message.reply(response, reply_markup=kb.tools_buttons)
        except Exception as e:
            print(f"Error getting weather for {city}: {e}")
            await message.reply(f"خطا در دریافت آب و هوای شهر '{city}'.", reply_markup=kb.tools_buttons)
        set_user_state(chat_id, st.UserState.NONE)

    elif current_state == st.UserState.AWAITING_MOBILE_SEARCH:
        await send_typing_action(bot, chat_id)
        query = message.text.strip()
        try:
            response = mobile(query)
            await message.reply(response, reply_markup=kb.tools_buttons)
        except Exception as e:
            print(f"Error searching mobile {query}: {e}")
            await message.reply("خطا در جستجوی موبایل.", reply_markup=kb.tools_buttons)
        set_user_state(chat_id, st.UserState.NONE)

    elif current_state == st.UserState.AWAITING_APARAT_SEARCH:
        await send_typing_action(bot, chat_id)
        query = message.text.strip()
        try:
            response = aparat(query)
            await message.reply(response, reply_markup=kb.tools_buttons)
        except Exception as e:
            print(f"Error searching Aparat for {query}: {e}")
            await message.reply("خطا در جستجوی آپارات.", reply_markup=kb.tools_buttons)
        set_user_state(chat_id, st.UserState.NONE)

    elif current_state == st.UserState.AWAITING_MUSIC_SEARCH:
        await send_typing_action(bot, chat_id)
        query = message.text.strip()
        try:
            response = music(query)
            await message.reply(response, reply_markup=kb.tools_buttons)
        except Exception as e:
            print(f"Error searching music for {query}: {e}")
            await message.reply("خطا در جستجوی خواننده.", reply_markup=kb.tools_buttons)
        set_user_state(chat_id, st.UserState.NONE)

    elif current_state == st.UserState.AWAITING_DIGIKALA_SEARCH:
        await send_typing_action(bot, chat_id)
        query = message.text.strip()
        try:
            response = digikala(query)
            await message.reply(response, reply_markup=kb.tools_buttons)
        except Exception as e:
            print(f"Error searching Digikala for {query}: {e}")
            await message.reply("خطا در جستجوی دیجی‌کالا.", reply_markup=kb.tools_buttons)
        set_user_state(chat_id, st.UserState.NONE)

    elif current_state == st.UserState.AWAITING_TRANSLATION_TEXT:
        await send_typing_action(bot, chat_id)
        try:
            translation = get_translate(message.text)
            await message.reply(f"📜 **متن ترجمه‌شده:**\n{translation}", reply_markup=kb.ai_services_buttons)
        except Exception as e:
            print(f"Error translating: {e}")
            await message.reply("خطایی در ترجمه رخ داد.", reply_markup=kb.ai_services_buttons)
        set_user_state(chat_id, st.UserState.NONE)

    elif current_state == st.UserState.AWAITING_BIRTHDATE:
        await send_typing_action(bot, chat_id)
        try:
            # اعتبارسنجی ساده فرمت تاریخ (می‌تواند کامل‌تر شود)
            parts = message.text.strip().split('/')
            if len(parts) == 3 and all(p.isdigit() for p in parts):
                 response = calculate_age(message.text.strip())
                 await message.reply(response, reply_markup=kb.tools_buttons)
                 set_user_state(chat_id, st.UserState.NONE)
            else:
                 await message.reply("🚫 فرمت تاریخ نامعتبر است. لطفا به صورت YYYY/MM/DD وارد کنید (مثال: 1374/02/04).")
                 # وضعیت کاربر تغییر نمی‌کند تا دوباره تلاش کند
        except Exception as e:
            print(f"Error calculating age: {e}")
            await message.reply("خطایی در محاسبه سن رخ داد. لطفا فرمت تاریخ را بررسی کنید.", reply_markup=kb.tools_buttons)
            set_user_state(chat_id, st.UserState.NONE)

    # --- حالت‌های گفتگو با AI ---
    elif current_state == st.UserState.CHATTING_AI_ASSISTANT:
        await send_typing_action(bot, chat_id)
        try:
            response = chat_with_ai(message.text) # دستیار مومن
            await message.reply(response, reply_markup=kb.Ai_back_button) # دکمه بازگشت به منوی AI
        except Exception as e:
            print(f"Error in chat_with_ai: {e}")
            await message.reply("⚠️ متاسفانه در ارتباط با دستیار مشکلی پیش آمد.", reply_markup=kb.Ai_back_button)
        # وضعیت حفظ می‌شود تا کاربر بتواند ادامه دهد

    elif current_state == st.UserState.CHATTING_GPT1:
        await send_typing_action(bot, chat_id)
        try:
            response = chat_with_ai_api(message.text, chat_id) # هوش مصنوعی حافظه‌دار
            await message.reply(response, reply_markup=kb.Ai_back_button)
        except Exception as e:
            print(f"Error in chat_with_ai_api: {e}")
            await message.reply("⚠️ متاسفانه در ارتباط با هوش مصنوعی مشکلی پیش آمد.", reply_markup=kb.Ai_back_button)

    elif current_state == st.UserState.CHATTING_GPT4:
        await send_typing_action(bot, chat_id)
        try:
            response = get_gpt(message.text) # ChatGPT-4o
            await message.reply(response, reply_markup=kb.Ai_back_button)
        except Exception as e:
            print(f"Error in get_gpt: {e}")
            await message.reply("⚠️ متاسفانه در ارتباط با ChatGPT مشکلی پیش آمد.", reply_markup=kb.Ai_back_button)

    elif current_state == st.UserState.CHATTING_LAWYER:
        await send_typing_action(bot, chat_id)
        try:
            response = chat_with_lawyer(message.text)
            await message.reply(response, reply_markup=kb.Ai_back_button)
        except Exception as e:
            print(f"Error in chat_with_lawyer: {e}")
            await message.reply("⚠️ متاسفانه در ارتباط با وکیل هوش مصنوعی مشکلی پیش آمد.", reply_markup=kb.Ai_back_button)

    elif current_state == st.UserState.CHATTING_PSYCHOLOGIST:
        await send_typing_action(bot, chat_id)
        try:
            response = chat_with_psychologist(message.text)
            await message.reply(response, reply_markup=kb.Ai_back_button)
        except Exception as e:
            print(f"Error in chat_with_psychologist: {e}")
            await message.reply("⚠️ متاسفانه در ارتباط با روانشناس هوش مصنوعی مشکلی پیش آمد.", reply_markup=kb.Ai_back_button)

    # --- حالت‌های ادمین ---
    elif current_state == st.UserState.AWAITING_BROADCAST_MESSAGE:
         if db.is_user_admin(chat_id): # فقط ادمین
             from utils.helpers import broadcast_message_content # وارد کردن متغیر موقت
             broadcast_message_content[chat_id] = message # ذخیره کل پیام برای ارسال احتمالی (شامل متن، عکس و...)
             await message.reply(
                 f"❓ آیا از ارسال این پیام به **{db.get_user_count()}** کاربر مطمئن هستید؟\n\n"
                 f"(پیش‌نمایش: {message.text[:100]}...)" if message.text else "(پیش‌نمایش: پیام شامل رسانه است)", # نمایش بخشی از متن
                 reply_markup=kb.confirm_broadcast_buttons
             )
             # وضعیت تغییر نمی‌کند تا تایید یا لغو شود
         else:
              set_user_state(chat_id, st.UserState.NONE) # کاربر عادی نباید در این وضعیت باشد

    elif current_state == st.UserState.AWAITING_ADMIN_USER_ID_TO_ADD:
         if db.is_user_admin(chat_id):
             try:
                 target_user_id = int(message.text.strip())
                 if db.set_admin_status(target_user_id, True):
                     await message.reply(f"✅ کاربر با آیدی {target_user_id} با موفقیت به لیست ادمین‌ها اضافه شد.", reply_markup=kb.admin_panel_buttons)
                     try: # اطلاع به کاربر جدید
                         await bot.send_message(target_user_id, "🎉 تبریک! شما توسط ادمین به لیست مدیران ربات اضافه شدید.")
                     except Exception:
                         await message.reply("⚠️ نتوانستم به کاربر جدید اطلاع دهم (ممکن است ربات را بلاک کرده باشد).")
                 else:
                     await message.reply(f"❌ کاربری با آیدی {target_user_id} یافت نشد یا خطایی رخ داد.", reply_markup=kb.admin_panel_buttons)
             except ValueError:
                 await message.reply("🚫 لطفا فقط آیدی عددی کاربر را وارد کنید.", reply_markup=kb.admin_panel_buttons)
             except Exception as e:
                 print(f"Error adding admin: {e}")
                 await message.reply("❌ خطایی در افزودن ادمین رخ داد.", reply_markup=kb.admin_panel_buttons)
             set_user_state(chat_id, st.UserState.NONE)
         else:
             set_user_state(chat_id, st.UserState.NONE)

    elif current_state == st.UserState.AWAITING_ADMIN_USER_ID_TO_REMOVE:
         if db.is_user_admin(chat_id):
              try:
                  target_user_id = int(message.text.strip())
                  if target_user_id in ADMIN_USER_IDS:
                      await message.reply("🚫 امکان حذف ادمین‌های اولیه تعریف شده در کانفیگ وجود ندارد.", reply_markup=kb.admin_panel_buttons)
                  elif db.set_admin_status(target_user_id, False):
                      await message.reply(f"✅ کاربر با آیدی {target_user_id} با موفقیت از لیست ادمین‌ها حذف شد.", reply_markup=kb.admin_panel_buttons)
                      try: # اطلاع به کاربر
                         await bot.send_message(target_user_id, "⚠️ شما توسط ادمین از لیست مدیران ربات حذف شدید.")
                      except Exception:
                         await message.reply("⚠️ نتوانستم به کاربر حذف شده اطلاع دهم.")
                  else:
                      await message.reply(f"❌ کاربری با آیدی {target_user_id} یافت نشد یا ادمین نبود.", reply_markup=kb.admin_panel_buttons)

              except ValueError:
                   await message.reply("🚫 لطفا فقط آیدی عددی کاربر را وارد کنید.", reply_markup=kb.admin_panel_buttons)
              except Exception as e:
                   print(f"Error removing admin: {e}")
                   await message.reply("❌ خطایی در حذف ادمین رخ داد.", reply_markup=kb.admin_panel_buttons)
              set_user_state(chat_id, st.UserState.NONE)
         else:
             set_user_state(chat_id, st.UserState.NONE)

    # --- اگر در هیچ وضعیتی نبود یا پیام نامرتبط بود ---
    # else:
        # می‌توانید یک پیام پیش‌فرض ارسال کنید یا نادیده بگیرید
        # await message.reply("دستور شما را متوجه نشدم. لطفا از دکمه‌ها استفاده کنید یا /start را بزنید.")
        # set_user_state(chat_id, st.UserState.NONE) # شاید بهتر باشد وضعیت ریست نشود
