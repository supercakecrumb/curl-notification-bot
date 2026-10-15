from .mytelebot import myTeleBot
from models.user import *
from telebot import types

MENU_CALLBACK_PREFIX = "test_"

def setup_button(bot: myTeleBot):
    @bot.message_handler(commands=['button'])
    def button_pressed(message: types.Message):
        bot.logger.info("Received bot command or message")
        markup = menu_markup()
        bot.send_message(message.chat.id, "Press a button if you want:", reply_markup=markup)

def menu_markup() -> types.InlineKeyboardMarkup:
    markup = types.InlineKeyboardMarkup()

    buttons = ([types.InlineKeyboardButton("button", callback_data=f"{MENU_CALLBACK_PREFIX}")])
    for b in buttons:
        markup.add(b)

    return markup

def handle_menu_callback(bot: myTeleBot, call: types.CallbackQuery):
    bot.answer_callback_query(callback_query_id=call.id, text="You definetely pressed a button", show_alert=False)
    pass
