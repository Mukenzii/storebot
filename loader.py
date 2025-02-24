from telebot import TeleBot, custom_filters
from telebot.storage import StateMemoryStorage

from config import *
from database import DataBase


bot = TeleBot(TOKEN, state_storage=StateMemoryStorage(), use_class_middlewares=True)

db = DataBase(DB_NAME, DB_PASSWORD, DB_HOST, DB_USER)


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.ChatFilter())
