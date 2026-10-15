import os
from dotenv import load_dotenv

load_dotenv()

token = os.environ.get("BOT_TOKEN")
sql_engine_url = os.environ.get("SQL_ENGINE_URL", "sqlite:///app.sqlite")
logging_config_path = os.environ.get("LOGGING_CONFIG_PATH", "logging.conf")
url = os.environ.get("URL", "0.0.0.0:80")
host = os.environ.get("HOST", "0.0.0.0")
port = os.environ.get("PORT", "80")
listen = os.environ.get("LISTEN", "0.0.0.0")
cert = os.environ.get("CERT")
priv = os.environ.get("PRIV")
webhook_url_path = os.environ.get("WEBHOOK_URL_PATH", "/api/web-hook/")
use_webhook = os.environ.get("USE_WEBHOOK", "false").lower() in {"true", "1", "yes"}
admin_password = os.environ.get("ADMIN_PASSWORD")
