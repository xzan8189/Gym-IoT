import os

class DefaultConfig:
    """ Web-site Configuration """

    # Flask
    SECRET_KEY = os.environ.get("Secret_key", "")

    # IFTTT
    IFTTT_EVENT_EMAIL_ERROR = os.environ.get("IFTTT_event_email_error", "")

    #Telegram bot
    BOT_TOKEN = os.environ.get("Bot_token", "")
    BOT_CHAT_ID = os.environ.get("Bot_chat_id", "")