"""
CODED BY SAIF KHAN:
Contact me: @Saitama_AU\n\n"
        "Join our Telegram group for support and updates: "
        "https://t.me/TechSaifTG
"""


import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace sensitive data with environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
USER_ID = int(os.environ.get('USER_ID'))
CHANNEL_A_ID = int(os.environ.get('CHANNEL_A_ID'))

def forward_message(update: Update, context: CallbackContext):
    try:
        destination_channel = context.args[0] if context.args else None
        if not destination_channel:
            update.message.reply_text("Please provide a destination channel.")
            return

        chat_id = int(destination_channel)
        if chat_id == CHANNEL_A_ID:
            update.message.reply_text("You cannot forward messages to Channel A.")
            return

        forwarded_message = update.message.forward(chat_id=chat_id)
        update.message.reply_text(f"Message forwarded to {destination_channel} successfully!")

    except ValueError:
        update.message.reply_text("Invalid channel ID provided.")
    except Exception as e:
        update.message.reply_text(f"Failed to forward the message. Error: {e}")

def help_command(update: Update, context: CallbackContext):
    help_text = (
        "Welcome to Telegram_msg bot!\n\n"
        "Available commands:\n"
        "/start - Start the bot and view a welcome message.\n"
        "/help - Display this help menu.\n"
        "/forward <destination_channel> - Forward the message to the specified channel."
    )
    update.message.reply_text(help_text)

def start_command(update: Update, context: CallbackContext):
    welcome_message = (
        "Hello there! I am Telegram_msg bot, your virtual assistant for group/channel management. "
        "🤖 Here to help you with real-time updates, media sharing, custom commands, and more! 🌟\n\n"
        "Contact me: @Saitama_AU\n\n"
        "Join our Telegram group for support and updates: "
        "https://t.me/TechSaifTG"
    )
    update.message.reply_text(welcome_message)

def main():
    # Set up your Telegram bot and handlers
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add your command handlers here
    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("forward", forward_message, pass_args=True))

    # Error handling for all other update types
    dp.add_error_handler(error_handler)

    # Start your bot
    updater.start_polling()
    updater.idle()

def error_handler(update: Update, context: CallbackContext):
    # Log the error
    print(f"An error occurred: {context.error}")

    # Inform the user about the error
    update.message.reply_text("Oops! Something went wrong. Please try again later.")

if __name__ == "__main__":
    main()
