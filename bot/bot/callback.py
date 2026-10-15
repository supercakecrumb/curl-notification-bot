from .mytelebot import myTeleBot
from models.user import *
from telebot import types
from .button import *

def setup_callback_queries(bot: myTeleBot):
    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call: types.CallbackQuery):
        bot.logger.info("Received callback")
        if call.message:
            if call.data.startswith("test_"):
                handle_menu_callback(bot, call)