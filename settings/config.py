import os

class DefaultConfig:
    """ Web-site Configuration """

    # Flask
    SECRET_KEY = os.environ.get("Secret_key", " ")

    # IFTTT
    IFTTT_EVENT_EMAIL_ERROR = os.environ.get("IFTTT_event_email_error", " ")