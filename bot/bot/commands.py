from .mytelebot import myTeleBot
from models.user import *
from .answers import *
from models.user import *
from .utils import sync_user
from config.bot import url



def setup_default_commands(bot: myTeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        sync_user(bot, message.from_user.id, message.from_user.username)
        bot.logger.info("Received bot command or message")
        bot.send_message(message.chat.id, start_text, parse_mode='Markdown', disable_web_page_preview=True)


    @bot.message_handler(commands=['help'])
    def send_help(message):
        sync_user(bot, message.from_user.id, message.from_user.username)
        bot.logger.info("Received bot command or message")
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown', disable_web_page_preview=True)


    @bot.message_handler(commands=["getbashscript"])
    def get_bash_script(message):
        if message.chat.type != "private":
            bot.send_message(message.chat.id, "Request your script in a private chat.")
            return
        user = sync_user(bot, message.from_user.id, message.from_user.username)
        bot.logger.info("Received bot command or message")
        bot.send_message(message.chat.id, bash_script.format(message.from_user.id, user.password, url), parse_mode='Markdown', disable_web_page_preview=True)


    @bot.message_handler(func=lambda m: True)
    def error(message):
        sync_user(bot, message.from_user.id, message.from_user.username)
        bot.logger.info("Received bot command or message")
        bot.reply_to(message, "Error!")
