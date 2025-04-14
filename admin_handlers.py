# handlers/admin_handlers.py
import asyncio
from balethon import Client
from balethon.objects import CallbackQuery, Message
import database as db
import keyboards as kb
import states as st
from helpers import set_user_state, broadcast_message_content, format_user_info
from config import ADMIN_USER_IDS # برای جلوگیری از حذف ادمین اصلی

async def handle_admin_callbacks(bot: Client, callback_query: CallbackQuery):
    """هندلر دکمه‌های اینلاین پنل ادمین"""
    user_id = callback_query.sender.id
    message = callback_query.message
    data = callback_query.data

    # --- بررسی اولیه: فقط ادمین ---
    if not db.is_user_admin(user_id):
        await callback_query.answer("🚫 دسترسی غیرمجاز", show_alert=True)
        return

    # --- دکمه‌های پنل ادمین ---
    if data == "admin_stats":
        total_users = db.get_user_count()
        # می‌توانید آمارهای بیشتری اضافه کنید (کاربران فعال، ...)
        await message.edit_text(
            f"📊 **آمار ربات:**\n\n"
            f"👤 تعداد کل کاربران: {total_users} نفر",
            reply_markup=kb.admin_panel_buttons
        )
        set_user_state(user_id, st.UserState.NONE)
        await callback_query.answer("آمار نمایش داده شد")

    elif data == "admin_broadcast":
        set_user_state(user_id, st.UserState.AWAITING_BROADCAST_MESSAGE)
        await message.edit_text(
            "📢 **ارسال پیام همگانی**\n\n"
            "لطفا پیامی که می‌خواهید به همه کاربران ارسال شود را بفرستید (متن، عکس، ویدیو و...).",
            reply_markup=kb.admin_panel_buttons # دکمه بازگشت به پنل
        )
        await callback_query.answer("منتظر دریافت پیام...")

    elif data == "confirm_broadcast":
        original_message = broadcast_message_content.get(user_id)
        if not original_message:
            await message.edit_text("❌ خطایی رخ داد: پیام اصلی برای ارسال یافت نشد.", reply_markup=kb.admin_panel_buttons)
            set_user_state(user_id, st.UserState.NONE)
            await callback_query.answer("خطا در ارسال", show_alert=True)
            return

        all_user_ids = db.get_all_user_ids()
        await message.edit_text(f"⏳ در حال ارسال پیام به {len(all_user_ids)} کاربر... لطفا صبور باشید.", reply_markup=None) # حذف دکمه‌ها هنگام ارسال

        success_count = 0
        fail_count = 0
        start_time = asyncio.get_event_loop().time()

        for target_id in all_user_ids:
            if target_id == user_id: continue # به خود ادمین ارسال نشود

            try:
                # ارسال کپی از پیام اصلی
                # توجه: Balethon ممکن است متد copy_message نداشته باشد.
                # اگر ندارد، باید نوع پیام را تشخیص داده و متد مناسب را فراخوانی کنید.
                if original_message.text:
                    await bot.send_message(target_id, original_message.text, entities=original_message.entities)
                elif original_message.photo:
                    # Balethon ممکن است نیاز به file_id یا ارسال مجدد فایل داشته باشد
                    # این بخش نیاز به تطبیق با نحوه کار Balethon با فایل‌ها دارد
                    await bot.send_photo(target_id, original_message.photo[-1].file_id, caption=original_message.caption, caption_entities=original_message.caption_entities)
                elif original_message.video:
                     await bot.send_video(target_id, original_message.video.file_id, caption=original_message.caption, caption_entities=original_message.caption_entities)
                # ... سایر انواع پیام (صدا، داکیومنت و...)
                else:
                    # اگر نوع پیام پشتیبانی نمی‌شود، حداقل متن را بفرستید
                     await bot.send_message(target_id, "شما یک پیام همگانی از طرف ادمین دریافت کردید.")

                success_count += 1
                print(f"Broadcast sent to {target_id}")
            except Exception as e:
                fail_count += 1
                print(f"Failed to send broadcast to {target_id}: {e}")
            await asyncio.sleep(0.1) # کمی تاخیر بین ارسال‌ها برای جلوگیری از محدودیت

        end_time = asyncio.get_event_loop().time()
        duration = round(end_time - start_time, 2)

        await message.edit_text(
            f"✅ **ارسال همگانی انجام شد.**\n\n"
            f"🔹 موفق: {success_count}\n"
            f"🔸 ناموفق: {fail_count}\n"
            f"⏱ مدت زمان: {duration} ثانیه",
            reply_markup=kb.admin_panel_buttons
        )
        broadcast_message_content.pop(user_id, None) # پاک کردن پیام موقت
        set_user_state(user_id, st.UserState.NONE)
        await callback_query.answer("ارسال کامل شد")


    elif data == "cancel_broadcast":
        broadcast_message_content.pop(user_id, None) # پاک کردن پیام موقت
        await message.edit_text("❌ ارسال پیام همگانی لغو شد.", reply_markup=kb.admin_panel_buttons)
        set_user_state(user_id, st.UserState.NONE)
        await callback_query.answer("عملیات لغو شد")

    elif data == "admin_add":
        set_user_state(user_id, st.UserState.AWAITING_ADMIN_USER_ID_TO_ADD)
        await message.edit_text("➕ **افزودن ادمین جدید**\n\nلطفا آیدی عددی کاربری که می‌خواهید به ادمین‌ها اضافه کنید را ارسال نمایید:", reply_markup=kb.admin_panel_buttons)
        await callback_query.answer("منتظر آیدی کاربر...")

    elif data == "admin_remove":
        set_user_state(user_id, st.UserState.AWAITING_ADMIN_USER_ID_TO_REMOVE)
        await message.edit_text("➖ **حذف ادمین**\n\nلطفا آیدی عددی ادمینی که می‌خواهید حذف کنید را ارسال نمایید:", reply_markup=kb.admin_panel_buttons)
        await callback_query.answer("منتظر آیدی کاربر...")

    # --- سایر دکمه‌های ادمین (مثلا مدیریت بن) ---
    # elif data == "admin_ban_list":
    #     # ... نمایش لیست کاربران بن شده و دکمه آنبن
    #     pass

    # --- پاسخ به callback query ---
    try:
        # برای دکمه‌هایی که فقط وضعیت را تغییر می‌دهند یا پیام را ویرایش می‌کنند
        if data not in ["confirm_broadcast"]: # ارسال همگانی خودش پیام ویرایش می‌کند
            await callback_query.answer()
    except Exception as e:
        print(f"Error answering admin callback query {callback_query.id}: {e}")

