import os
os.environ["SQL_ENGINE_URL"] = "sqlite:///:memory:"
import unittest
from unittest.mock import Mock, patch
from types import SimpleNamespace
from flask import Flask

from bot.bot import init_flask
from bot.utils import authenticate

class NotificationSecurityTests(unittest.TestCase):
    def test_per_user_password_required(self):
        user = SimpleNamespace(password="test-password-not-a-real-credential")
        with patch("bot.utils.get_user_by_tg_id", return_value=user) as lookup:
            self.assertFalse(authenticate("5", None))
            self.assertFalse(authenticate("not-numeric", user.password))
            self.assertFalse(authenticate("5", "wrong"))
            self.assertTrue(authenticate("5", user.password))
            lookup.assert_called_with(5)
        with patch("bot.utils.get_user_by_tg_id", return_value=None):
            self.assertFalse(authenticate("6", user.password))

    def test_http_rejects_forged_and_accepts_valid_notification(self):
        app = Flask(__name__)
        bot = Mock()
        with patch.object(app, "run") as run:
            init_flask(bot, app, "127.0.0.1", 80)
        self.assertFalse(run.call_args.kwargs["debug"])
        client = app.test_client()
        user = SimpleNamespace(password="test-password-not-a-real-credential")
        with patch("bot.utils.get_user_by_tg_id", return_value=user):
            self.assertEqual(client.post("/send_notification", json={"text":"hi","telegram_id":"5","password":"wrong"}).status_code, 401)
            bot.send_message.assert_not_called()
            self.assertEqual(client.post("/send_notification", json={"text":"hi","telegram_id":"5","password":user.password}).status_code, 200)
            bot.send_message.assert_called_once_with("5", "hi")
        self.assertEqual(client.post("/send_notification", json=[]).status_code, 400)

class AdminSecurityTests(unittest.TestCase):
    def test_missing_password_and_group_enrollment_are_denied(self):
        from bot.admin import setup_admin_commands
        handlers = {}
        bot = Mock()
        def register(**kwargs):
            def decorate(fn):
                handlers[kwargs["commands"][0]] = fn
                return fn
            return decorate
        bot.message_handler.side_effect = register
        setup_admin_commands(bot)
        message = SimpleNamespace(chat=SimpleNamespace(id=1,type="private"), from_user=SimpleNamespace(id=1,username="tester"),text="/become_admin")
        with patch("bot.admin.admin_password", None):
            handlers["become_admin"](message)
        bot.register_next_step_handler.assert_not_called()
        message.chat.type = "group"
        with patch("bot.admin.admin_password", "test-admin-password"):
            handlers["become_admin"](message)
        bot.register_next_step_handler.assert_not_called()

if __name__ == "__main__":
    unittest.main()
