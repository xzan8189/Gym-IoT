import os

class DefaultConfig:
    """ Web-site Configuration """

    # Flask
    SECRET_KEY = os.environ.get("Secret_key", "")

    # IFTTT
    IFTTT_EVENT_EMAIL_ERROR = os.environ.get("IFTTT_event_email_error", "")

    #Telegram bot
    BOT_TOKEN = os.environ.get("Bot_token", "")
    BOT_TOKEN_PAYMENT_PROVIDER = os.environ.get("Bot_token_payment_provider", "")