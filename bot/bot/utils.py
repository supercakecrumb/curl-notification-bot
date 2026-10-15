
import secrets, string
from models.user import get_user_by_tg_id, save_new_user
from .mytelebot import myTeleBot
from models.user import get_admins, User


botForUtil = None
def init_util_bot(bot: myTeleBot):
    global botForUtil
    botForUtil = bot

  
def admin_only(func):
    def wrapper(message):
        if message.chat.type != "private":
            botForUtil.send_message(message.chat.id, "Use a private chat for admin commands.")
            return
        client = get_user_by_tg_id(message.from_user.id)
        if client is None or (not client.is_admin):
            botForUtil.send_message(message.chat.id, "You can't do it!")
            return
        return func(message)
    return wrapper

def sync_user(bot: myTeleBot, user_id: int, username: str) -> User:
    user = get_user_by_tg_id(user_id)
    if user is None:
        user = save_new_user(user_id, username, generate_password())
        send_notification_to_admins(bot, username)
    return user


def send_notification_to_admins(bot: myTeleBot, new_user_username: str):
    admins = get_admins()
    for admin in admins:
        bot.send_message(admin.tg_id, f'New user - @{new_user_username}')


def generate_password(length=20):
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for i in range(length))
    return password


def authenticate(telegram_id: str, password: str):
    if not isinstance(password, str) or not password:
        return False
    try:
        user_id = int(telegram_id)
    except (TypeError, ValueError):
        return False
    user = get_user_by_tg_id(user_id)
    return bool(user and user.password and secrets.compare_digest(
        password.encode(), user.password.encode()))