import datetime
import json
import re

import boto3
from botocore.exceptions import ClientError
from telegram import LabeledPrice, ForceReply
from telegram.ext import PreCheckoutQueryHandler, ConversationHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.update import Update

from settings.config import DefaultConfig

# Instance variables
CONFIG = DefaultConfig()
sfn_client = boto3.client('stepfunctions', endpoint_url="http://localhost:4566")
state_machine_arn = CONFIG.STATE_MACHINE_ARN
dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:4566")
table_users = dynamodb.Table('Users')

updater = Updater(CONFIG.BOT_TOKEN, use_context=True)
EXPECT_NAME = range(1)


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

            if user_found_dict['telegram_chat_id'] == "":  # Checking if the customer has already registered his chat_id of Telegram on the platform
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


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :
	/pay - Pay the month to continue using our services!
	/gym_iot - To login on the Website
	/gym_iot_registration - Sign-up on the Website!""")


def pay(update: Update, context: CallbackContext):
    email = update.message.text
    context.user_data['email'] = email
    username = update.message.from_user.username.lower()
    context.user_data['username'] = username

    try:
        user_found_dict = table_users.get_item(Key={'username': username.lower()})

        if len(user_found_dict) > 1: # User found in DB
            user_found_dict = user_found_dict['Item']

            # The customer has just registered on the platform
            if user_found_dict['payment']['last_time_paid'] == "":
                sending_invoice(update, context)
            else:
                # Checking if the customer has to pay
                date_format = '%Y-%m-%d'
                a = datetime.datetime.strptime(datetime.datetime.today().strftime('%Y-%m-%d'), date_format)
                b = datetime.datetime.strptime(user_found_dict['payment']['last_time_paid'], date_format)
                delta = a - b
                if delta.days >= 31: # The customer has to pay
                    sending_invoice(update, context)
                else: # The customer already paid
                    update.message.reply_text(f"💪🏻 Hi {username}, You have already paid this month!")

                print("Days: " + str(delta.days))
        else:  # User not found in DB
            print("User not found")
            update.message.reply_text(f"☹ You are NOT registered on the web site {username}! Try to use this command instead /gym_iot_registration to register your new account 🦾")

    except ClientError as e:
        print(e.response['Error']['Message'])

    # ends this particular conversation flow
    return ConversationHandler.END

def email_input_by_user(update: Update, context: CallbackContext):
    update.message.reply_text('✍ Insert your email to send the billing!')

    return EXPECT_NAME

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Conversation cancelled by user. Bye. Send /pay to start again')
    return ConversationHandler.END

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

# Payment functions
def precheckout_callback(update: Update, context: CallbackContext) -> None:
    # Data to send
    username = context.user_data['username']
    email_customer = context.user_data['email']

    # Checking if the email is correct
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    query = update.pre_checkout_query
    if re.fullmatch(regex, email_customer) == None:
        query.answer(ok=False, error_message=f"The email '{email_customer}' is not correct.")

    payment_amount = int(query.total_amount / 100)
    tip = False
    tip_amount = 0

    if payment_amount > 70:
        tip_amount = payment_amount - 70
        tip = True
    print(f"payment_amount: {payment_amount}, tip_amount: {tip_amount}")

    sfn_client.describe_state_machine(
        stateMachineArn=state_machine_arn
    )

    # Start execution of Step Functions
    response = sfn_client.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps({'Tip': tip,
                          'username': username,
                          'payment_amount': payment_amount,
                          'tip_amount': tip_amount,
                          'email_customer': email_customer})
    )

    query.answer(ok=True)


def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    # Updating the date of the last payment
    username = update.message.from_user.username
    user_found_dict = table_users.get_item(Key={'username': username.lower()})
    user_found_dict = user_found_dict['Item']
    user_found_dict['payment']['last_time_paid'] = datetime.datetime.today().strftime('%Y-%m-%d')
    table_users.put_item(Item=user_found_dict)

    msg_id = update.message.reply_text(f"Thank you for your payment!🥳\nWe also sent an 📧mail to {context.user_data['email']}").message_id
    update.message.chat.pin_message(msg_id)

def sending_invoice(update, context):
    # Send invoice
    title = "GymIoT Payment"
    description = "This is the monthly payment to be paid to continue using all the services made available by the gym.\n" \
                  "Below you will see in detail what you are paying for."
    payload = "Custom-Payload"
    currency = "USD"
    price = 100
    prices = [LabeledPrice("Machines", price * 50), LabeledPrice("Shower", price * 20)]

    context.bot.send_invoice(
        update.message.chat_id,
        title,
        description,
        payload,
        CONFIG.BOT_TOKEN_PAYMENT_PROVIDER,
        max_tip_amount=price * 15,
        suggested_tip_amounts=[price * 5, price * 10, price * 15],
        photo_url="https://raw.githubusercontent.com/xzan8189/Gym-IoT/master/website/static/img/payment_image.jpeg?token=GHSAT0AAAAAABOM7ERS6VUBXIUEJJS2QMBIYWLCBBQ",
        photo_height=512,
        photo_width=512,
        photo_size=512,
        currency=currency,
        prices=prices,
        is_flexible=False
    )





updater.dispatcher.add_handler(CommandHandler('start', start))

updater.dispatcher.add_handler(ConversationHandler(
    entry_points=[CommandHandler('pay', email_input_by_user)],
    states={
        EXPECT_NAME: [MessageHandler(Filters.text, pay)],
    },
    fallbacks=[CommandHandler('cancel', cancel)]
))

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
