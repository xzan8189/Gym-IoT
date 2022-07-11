import boto3
from botocore.exceptions import ClientError
from telegram import LabeledPrice
from telegram.ext import PreCheckoutQueryHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.update import Update

from settings.config import DefaultConfig

# Instance variables
CONFIG = DefaultConfig()
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table_users = dynamodb.Table('Users')

updater = Updater(CONFIG.BOT_TOKEN, use_context=True)


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    update.message.reply_text(f"⭐️Hello {user.username}, welcome to the *GymIoT_bot*!", parse_mode='Markdown')
    update.message.reply_text("Wait for a moment.. I'm finding you on the platform... 🤖")

    # Finding user in database
    try:
        user_found_dict = table_users.get_item(Key={'username': user.username.lower()})
        if len(user_found_dict) > 1:
            print("User found!")
            update.message.reply_text("*Found!*", parse_mode='Markdown')
            user_found_dict = user_found_dict['Item']

            if user_found_dict[
                'telegram_chat_id'] == "":  # Checking if the custmer has already registered his chat_id of Telegram on the platform
                user_found_dict['telegram_chat_id'] = str(user.id)
                table_users.put_item(Item=user_found_dict)  # Updating the customer with his chat_id of Telegram

                update.message.reply_text(
                    f"*All done!*\n"
                    f"From now on you will receive all the necessary notifications to achieve a good workout! 🏋️\n"
                    f"Please write /help to see the commands available.", parse_mode='Markdown')
            else:
                update.message.reply_text(
                    f"You are already registered {user.username}! Try to not use this command, it is stressful for me 😮‍💨")
        else:  # User not found in DB
            print("User not found")
            update.message.reply_text(
                f"☹ You are NOT registered on the web site {user.username}! Try to use this command instead /gym_iot_registration to register your new account 🦾")

    except ClientError as e:
        print(e.response['Error']['Message'])


    # print(update.message.from_user)
    # print(update.message.chat.id)
    # print(user.id)

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :
	/gym_iot - To login on the Website
	/gym_iot_registration - Sign-up on the Website!""")

    title = "TITLE"
    description = "description"
    payload = "Custom-Payload"
    currency = "USD"
    price = 100
    prices = [LabeledPrice("Machines", price * 40), LabeledPrice("Shower", price * 20)]

    context.bot.send_invoice(
        update.message.chat_id,
        title,
        description,
        payload,
        CONFIG.BOT_TOKEN_PAYMENT_PROVIDER,
        max_tip_amount=100000,
        suggested_tip_amounts=[price * 10, price * 15, price * 20],
        photo_url="https://raw.githubusercontent.com/xzan8189/Gym-IoT/master/website/static/img/payment_image.jpeg?token=GHSAT0AAAAAABOM7ERS6VUBXIUEJJS2QMBIYWLCBBQ",
        photo_height=512,
        photo_width=512,
        photo_size=512,
        currency=currency,
        prices=prices,
        is_flexible=False
    )


def gym_iot_url(update: Update, context: CallbackContext):
    update.message.reply_text("Website Login Link =>\
	[Gym_IoT Login](http://127.0.0.1:5000/login)", parse_mode='Markdown')


def gym_iot_signup_url(update: Update, context: CallbackContext):
    update.message.reply_text("Website Registration Link =>\
	[Gym_IoT Sign-up](http://127.0.0.1:5000/sign-up)", parse_mode='Markdown')


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)


# Payment
def precheckout_callback(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    query.answer(ok=False, error_message=f"invoice_payload: {query.invoice_payload},\n"
                                         f"order_info: {query.order_info},\n"
                                         f"total_amount: {str(query.total_amount/100)},\n"
                                         f"shipping_option_id: {str(query.shipping_option_id)}")


def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Thank you for your payment!")


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('gym_iot', gym_iot_url))
updater.dispatcher.add_handler(CommandHandler('gym_iot_registration', gym_iot_signup_url))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands

updater.dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
updater.dispatcher.add_handler(
    MessageHandler(Filters.successful_payment, successful_payment_callback)
)

# Start Bot
updater.start_polling()
