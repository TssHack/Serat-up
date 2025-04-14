# states.py
from enum import Enum, auto

class UserState(Enum):
    # حالت‌های عادی
    NONE = auto() # حالت پیش‌فرض یا بعد از اتمام کار
    AWAITING_PRAYER_CITY = auto()
    AWAITING_FONT_TEXT = auto()
    AWAITING_WEATHER_CITY = auto()
    AWAITING_TRACKING_CODE = auto()
    AWAITING_MOBILE_SEARCH = auto()
    AWAITING_APARAT_SEARCH = auto()
    AWAITING_DIGIKALA_SEARCH = auto()
    AWAITING_MUSIC_SEARCH = auto()
    AWAITING_TRANSLATION_TEXT = auto()
    AWAITING_BIRTHDATE = auto()

    # حالت‌های گفتگو با AI
    CHATTING_AI_ASSISTANT = auto() # دستیار مومن
    CHATTING_GPT1 = auto()         # هوش مصنوعی حافظه دار
    CHATTING_GPT4 = auto()         # ChatGPT-4o
    CHATTING_LAWYER = auto()
    CHATTING_PSYCHOLOGIST = auto()

    # حالت‌های ادمین
    AWAITING_BROADCAST_MESSAGE = auto()
    AWAITING_ADMIN_USER_ID_TO_ADD = auto()
    AWAITING_ADMIN_USER_ID_TO_REMOVE = auto()
    # ... سایر وضعیت‌های ادمین
