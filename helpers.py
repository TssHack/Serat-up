# utils/helpers.py
import asyncio
from balethon import Client

user_states = {} # دیکشنری وضعیت کاربران (در حافظه موقت)
# --- می‌توانید این بخش را پیشرفته‌تر کنید ---
# مثلا با استفاده از دیتابیس یا یک کتابخانه مدیریت وضعیت

# داده موقت برای پیام همگانی (می‌تواند در دیتابیس ذخیره شود)
broadcast_message_content = {}

async def send_typing_action(bot: Client, chat_id):
    """ارسال اکشن تایپینگ"""
    try:
        await bot.send_chat_action(chat_id, "typing")
        await asyncio.sleep(0.5) # کمی تاخیر برای نمایش بهتر
    except Exception as e:
        print(f"Error sending typing action to {chat_id}: {e}")

def set_user_state(user_id, state):
    """تنظیم وضعیت کاربر"""
    if state is None or state == UserState.NONE:
        user_states.pop(user_id, None) # حذف وضعیت قبلی
    else:
        user_states[user_id] = state
    # print(f"State for {user_id} set to: {state}") # برای دیباگ

def get_user_state(user_id):
    """دریافت وضعیت فعلی کاربر"""
    return user_states.get(user_id, UserState.NONE)

# --- توابع کمکی دیگر ---
def format_user_info(user):
    """فرمت نمایش اطلاعات کاربر"""
    name = user.first_name
    if user.last_name:
        name += f" {user.last_name}"
    if user.username:
        name += f" (@{user.username})"
    return name
