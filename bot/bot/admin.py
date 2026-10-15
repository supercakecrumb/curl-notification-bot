import hmac
from .utils import admin_only
from .mytelebot import myTeleBot
from models.user import *
from config.bot import admin_password

def setup_admin_commands(bot: myTeleBot):
    @bot.message_handler(commands=['become_admin'])
    def assign_admin(message):
        bot.logger.info("Received bot command or message")
        if message.chat.type != "private" or not admin_password:
            bot.send_message(message.chat.id, "Admin enrollment is unavailable here.")
            return
        callback = bot.send_message(message.chat.id, "Please enter the password to receive admin rights")
        bot.register_next_step_handler(callback, receive_password)

    def receive_password(message):
        if (message.chat.type == "private" and admin_password and
                isinstance(message.text, str) and
                hmac.compare_digest(message.text.encode(), admin_password.encode())):
            user = get_user_by_tg_id(message.from_user.id)
            if user is not None:
                grant_user_admin_role(user)
                bot.logger.info(f'{message.from_user.username} received admin rights')
                bot.send_message(message.chat.id, "Now you're admin!")
        else:
            bot.send_message(message.chat.id, "Wrong password! Fuck off")
        bot.delete_message(message.chat.id, message.message_id)


    @bot.message_handler(commands=['users'])
    @admin_only
    def list_users(message):
        bot.logger.info("Received bot command or message")
        users = get_users()
        out = "\n".join(map(repr, users))
        bot.send_message(message.chat.id, "Found users:\n" + out)

