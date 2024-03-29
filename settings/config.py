import os

class DefaultConfig:
    """ Web-site Configuration """

    # Flask
    SECRET_KEY = os.environ.get("Secret_key", "")

    #Telegram bot
    BOT_TOKEN = os.environ.get("Bot_token", "")
    BOT_TOKEN_PAYMENT_PROVIDER = os.environ.get("Bot_token_payment_provider", "")

    # AWS SeS
    EMAIL_OWNER = os.environ.get("Email_owner", "")

    # AWS Step Functions
    STATE_MACHINE_ARN = os.environ.get("State_machine_arn", "")