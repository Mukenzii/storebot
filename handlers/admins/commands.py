from telebot.types import Message

from loader import bot
from config import ADMINS
from keyboards.default import admin_btn


@bot.message_handler(commands=['start'], chat_id=ADMINS)
def admin_start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, "Salom admin", reply_markup=admin_btn())












