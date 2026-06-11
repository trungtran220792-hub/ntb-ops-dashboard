import os
from dotenv import load_dotenv
load_dotenv(override=True)
print("CONSOLIDATED_URL:", os.environ.get("CONSOLIDATED_URL"))
print("TELEGRAM_BOT_TOKEN:", os.environ.get("TELEGRAM_BOT_TOKEN"))
