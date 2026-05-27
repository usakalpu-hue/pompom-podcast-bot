# pompombot.py
# VIP Podcast Telegram Bot With Admin Panel

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

# ================== CONFIG ==================

API_ID = 22146561
API_HASH = "031377061c6714e885782314c414dcd1"
BOT_TOKEN = "8643810259:AAFOGKJ4kAT93Mofdx-DLvmgutI_7bc4dTU"

ADMIN_ID = 8766444295

# ============================================

bot = Client(
    "PomPomBot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ================= DATABASE =================

db = sqlite3.connect("pompom.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER
)
""")

db.commit()

# ================= FUNCTIONS =================

def add_user(user_id):
    cursor.execute(
        "SELECT * FROM users WHERE user_id=?",
        (user_id,)
    )

    data = cursor.fetchone()

    if data is None:
        cursor.execute(
            "INSERT INTO users VALUES(?)",
            (user_id,)
        )
        db.commit()

def get_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

# ================= START =================

@bot.on_message(filters.command("start"))
async def start(client, message):

    add_user(message.from_user.id)

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🎙 Podcast",
                callback_data="podcast"
            )
        ],
        [
            InlineKeyboardButton(
                "💎 VIP Plans",
                callback_data="plans"
            )
        ],
        [
            InlineKeyboardButton(
                "👑 Admin Panel",
                callback_data="admin"
            )
        ]
    ])

    await message.reply_text(
        f"""
👋 Hello {message.from_user.first_name}

🎙 Welcome To PomPom Podcast Bot

✅ Daily Podcast
✅ VIP Access
✅ Premium Features
✅ Admin System
        """,
        reply_markup=buttons
    )

# ================= CALLBACKS =================

@bot.on_callback_query()
async def callbacks(client, query):

    data = query.data

    # Podcast Button
    if data == "podcast":

        await query.message.reply_audio(
            audio="podcast.mp3",
            title="New Podcast",
            performer="KALPU PODCAST"
        )

    # VIP Plans
    elif data == "plans":

        await query.message.reply_text(
            """
💎 VIP Plans

🔥 30 Days = ₹99
🔥 90 Days = ₹199
🔥 365 Days = ₹499

📩 Contact Admin For Purchase
            """
        )

    # Admin Panel
    elif data == "admin":

        if query.from_user.id != ADMIN_ID:
            return await query.answer(
                "❌ You Are Not Admin",
                show_alert=True
            )

        total_users = len(get_users())

        admin_buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "📢 Broadcast",
                    callback_data="broadcast"
                )
            ],
            [
                InlineKeyboardButton(
                    "📊 Stats",
                    callback_data="stats"
                )
            ]
        ])

        await query.message.reply_text(
            f"""
👑 ADMIN PANEL

👥 Total Users: {total_users}
            """,
            reply_markup=admin_buttons
        )

    # Stats
    elif data == "stats":

        total_users = len(get_users())

        await query.message.reply_text(
            f"📊 Total Users: {total_users}"
        )

# ================= BROADCAST =================

broadcast_mode = {}

@bot.on_message(filters.command("broadcast") & filters.user(ADMIN_ID))
async def broadcast(client, message):

    broadcast_mode[message.from_user.id] = True

    await message.reply_text(
        "📢 Send Message To Broadcast"
    )

@bot.on_message(filters.private)
async def handle_message(client, message):

    user_id = message.from_user.id

    if user_id in broadcast_mode:

        users = get_users()

        sent = 0

        for user in users:
            try:
                await message.copy(user[0])
                sent += 1
            except:
                pass

        del broadcast_mode[user_id]

        await message.reply_text(
            f"✅ Broadcast Sent To {sent} Users"
        )

# ================= RUN =================

print("✅ PomPom Bot Started")
bot.run()
      
