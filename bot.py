import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time

# Load secrets from environment
BOT_TOKEN = os.environ['8386329255:AAHI_yzX-mbQod8rIgbzDxF9lzEBSyV-k7s']
CHANNELS = [int(os.environ['2865152421']), int(os.environ['2769878360'])]
CHANNEL_LINKS = [os.environ['https://t.me/+Xhj0O9GjRLczNjVi'], os.environ['https://t.me/+lVyoBLl7IVFjMTIy']]

bot = telebot.TeleBot(BOT_TOKEN)

def check_user_channels(user_id):
    for channel in CHANNELS:
        try:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
            time.sleep(0.3)  # avoid rate-limiting
        except Exception:
            return False
    return True

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    for i, link in enumerate(CHANNEL_LINKS, start=1):
        markup.add(InlineKeyboardButton(f"{i} - kanal", url=link))
    markup.add(InlineKeyboardButton("✅ Tasdiqlash", callback_data="check"))
    
    bot.send_message(
        message.chat.id,
        "❌ Kechirasiz, botdan foydalanishdan oldin quyidagi kanallarga a'zo bo'lishingiz kerak.",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data == "check")
def callback_check(call):
    user_id = call.from_user.id
    if check_user_channels(user_id):
        bot.send_message(call.message.chat.id, "✅ Rahmat! Siz barcha kanallarga a'zo bo'lgansiz.")
    else:
        markup = InlineKeyboardMarkup()
        for i, link in enumerate(CHANNEL_LINKS, start=1):
            markup.add(InlineKeyboardButton(f"{i} - kanal", url=link))
        markup.add(InlineKeyboardButton("✅ Qaytadan tekshirish", callback_data="check"))

        bot.send_message(
            call.message.chat.id,
            "❌ Siz hali ham barcha kanallarga a'zo bo'lmadingiz. Iltimos, a'zo bo'lib qayta urinib ko'ring.",
            reply_markup=markup
        )

bot.infinity_polling(timeout=10, long_polling_timeout=5)