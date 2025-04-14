# database.py
import sqlite3
import datetime
from config import DATABASE_NAME

def get_db_connection():
    """ایجاد یا اتصال به پایگاه داده"""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # دسترسی به ستون‌ها با نام
    return conn

def initialize_database():
    """ایجاد جداول اولیه در صورت عدم وجود"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            last_name TEXT,
            username TEXT,
            join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_admin INTEGER DEFAULT 0,
            is_banned INTEGER DEFAULT 0,
            last_activity TIMESTAMP
        )
    ''')
    # می‌توانید جدول دیگری برای لاگ فعالیت‌ها اضافه کنید
    # cursor.execute('''
    #     CREATE TABLE IF NOT EXISTS activity_log (
    #         log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    #         user_id INTEGER,
    #         timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    #         action TEXT,
    #         details TEXT,
    #         FOREIGN KEY (user_id) REFERENCES users (user_id)
    #     )
    # ''')
    conn.commit()
    conn.close()
    print("Database initialized successfully.")

def add_or_update_user(user_id, first_name, last_name, username):
    """اضافه کردن کاربر جدید یا آپدیت اطلاعات و زمان آخرین فعالیت"""
    conn = get_db_connection()
    cursor = conn.cursor()
    now = datetime.datetime.now()
    cursor.execute('''
        INSERT INTO users (user_id, first_name, last_name, username, last_activity)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(user_id) DO UPDATE SET
            first_name = excluded.first_name,
            last_name = excluded.last_name,
            username = excluded.username,
            last_activity = excluded.last_activity
    ''', (user_id, first_name, last_name, username, now))
    conn.commit()
    conn.close()

def is_user_admin(user_id):
    """بررسی اینکه آیا کاربر ادمین است یا خیر"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT is_admin FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result and result['is_admin'] == 1

def set_admin_status(user_id, is_admin: bool):
    """تنظیم وضعیت ادمین برای کاربر"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE users SET is_admin = ? WHERE user_id = ?', (1 if is_admin else 0, user_id))
    updated = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return updated

def get_user_count():
    """دریافت تعداد کل کاربران"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users')
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_all_user_ids():
    """دریافت لیست تمام user_id ها"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE is_banned = 0') # فقط کاربران بن نشده
    user_ids = [row['user_id'] for row in cursor.fetchall()]
    conn.close()
    return user_ids

# --- توابع دیگر مورد نیاز پنل ادمین ---
def get_banned_users():
    # ... (برای نمایش کاربران بن شده)
    pass

def ban_user(user_id):
    # ... (برای بن کردن کاربر)
    pass

def unban_user(user_id):
    # ... (برای آنبن کردن کاربر)
    pass

# Initialize database on first import
initialize_database()
