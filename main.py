"""
CODED BY SAIF KHAN:
Contact me: @Saitama_AU\n\n"
        "Join our Telegram group for support and updates: "
        "https://t.me/TechSaifTG
"""

import os
from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Replace sensitive data with environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
USER_ID = int(os.getenv('CHAT_ID'))

last_forwarded_message_id = None

def forward_message(update: Update, context: CallbackContext):
    try:
        destination_channel = context.args[0] if context.args else None
        if not destination_channel:
            update.message.reply_text("Please provide a destination's channel CHAT_ID, eg: /forward 123456789.")
            return

        chat_id = int(destination_channel)
        forwarded_message = update.message.forward(chat_id=chat_id)
        update.message.reply_text(f"Message forwarded to {destination_channel} successfully!")

    except ValueError:
        update.message.reply_text("Invalid channel ID provided.")
    except Exception as e:
        update.message.reply_text(f"Failed to forward the message. Error: {e}")

def forward_old_messages(update: Update, context: CallbackContext):
    try:
        destination_channel = context.args[0] if context.args else None
        if not destination_channel:
            update.message.reply_text("Please provide a destination's channel ID, eg: /forward 123456789.")
            return

        chat_id = int(destination_channel)

        global last_forwarded_message_id

        # Fetch and forward older messages
        messages = update.message.chat.get_chat_history(limit=100, offset_id=last_forwarded_message_id)
        for message in messages:
            # Skip deleted messages, polls, contacts, and locations
            if message.delete_for_all or message.poll or message.contact or message.location:
                continue

            # Check if the message contains media files
            if message.photo:
                message.photo[-1].forward(chat_id=chat_id)
            elif message.video:
                message.video.forward(chat_id=chat_id)
            elif message.audio:
                message.audio.forward(chat_id=chat_id)
            elif message.voice:
                message.voice.forward(chat_id=chat_id)
            elif message.sticker:
                message.sticker.forward(chat_id=chat_id)
            # Add more conditions for other media types (documents, animations, etc.) if needed

            # Update the last forwarded message ID
            last_forwarded_message_id = message.message_id

        if messages:
            update.message.reply_text(f"Batch of 100 messages forwarded to {destination_channel} successfully!")
        else:
            update.message.reply_text("No more messages to forward.")

    except ValueError:
        update.message.reply_text("Invalid channel ID provided.")
    except Exception as e:
        update.message.reply_text(f"Failed to forward messages. Error: {e}")

def help_command(update: Update, context: CallbackContext):
    help_text = (
        "Welcome to Telegram_msg bot!\n\n"
        "Available commands:\n"
        "/start - Start the bot and view a welcome message.\n"
        "/help - Display this help menu.\n"
        "/forward <destination_channel> - Forward the message to the specified channel.\n"
        "/old_msg <destination_channel> - Forward older messages with media files to the specified channel."
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
    dp.add_handler(CommandHandler("old_msg", forward_old_messages, pass_args=True))

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

