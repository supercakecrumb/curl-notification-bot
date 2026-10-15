from .mytelebot import myTeleBot
from .admin import setup_admin_commands
from .commands import setup_default_commands
from .callback import setup_callback_queries
from .utils import authenticate
from flask import Flask, request
import time


def init_bot(bot: myTeleBot):
    bot.remove_webhook()
    time.sleep(0.1)
    bot.logger.info("Bot initialized.")


def init_flask(bot: myTeleBot, app: Flask, listen: str, port: int):
    app.config['MAX_CONTENT_LENGTH'] = 64 * 1024

    @app.route('/', methods=['GET', 'HEAD'])
    def index():
        return 'hey, howrudoing?'

    @app.route('/send_notification', methods=['POST'])
    def send_notification():
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return "Invalid JSON", 400
        text = data.get('text')
        telegram_id = data.get('telegram_id')
        telegram_password = data.get('password')

        if not isinstance(text, str) or not text or len(text) > 4096:
            return "Invalid message", 400
        if authenticate(telegram_id, telegram_password):
            send_telegram_notification(telegram_id, text)
            return 'Notification sent successfully'
        else:
            return 'Authentication failed', 401
        
    def send_telegram_notification(telegram_id: str, text: str):
        bot.send_message(telegram_id, text)

    app.run(host=listen,
            port=port,
            debug=False)


def init_message_handlers(bot: myTeleBot):
    bot.logger.debug("init_message_handlers")
    setup_admin_commands(bot)
    setup_default_commands(bot)
    setup_callback_queries(bot)

