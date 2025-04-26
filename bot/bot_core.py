import os, asyncio, signal, sys

from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv

from models.schema import DutchEnglishVocab
from models.db_setup import Session      #we import it from db_setup.py, where the main setup is written
from bot.bot_commands import (
    add_handler,
    list_handler,
    delete_handler,
    edit_handler,
    get_handler,
    search_handler,
    help_handler,
    practice_handler,
    stop_practice_handler,
    set_practice_mode,
    answer_handler
)

#print("✅ Imported handlers from bot_commands:")
#print(practice_handler)
#print(stop_practice_handler)
#print(set_practice_mode)
#print(answer_handler)


load_dotenv() #Loads variables from .env file into memory
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN") # Grab the token from memory and store it in the variable BOT_TOKEN

##        python -m bot.bot_core       - start##
##        CTRL C       - end##

# Graceful shutdown

def signal_handler(sig, frame):
    print('🤖 Bot is stopping gracefully...')
    sys.exit(0) #Exit the program
    
signal.signal(signal.SIGINT, signal_handler)


# Start Command Handler
async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I am WiseWord, or WW, your bot. Send /stop to stop me.")
    
    
# Stop Command Handler
async def stop_handler(update:Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(("🤖 Bot is stopping gracefully... Bye!Until next time!"))
    await context.application.shutdown() # Gracefully stops the bot


# Initialize the bot
def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build() 

    app.add_handler(CommandHandler("start", start_handler))
    app.add_handler(CommandHandler("stop", stop_handler))
    app.add_handler(CommandHandler("add", add_handler))
    app.add_handler(CommandHandler("list", list_handler))   
    app.add_handler(CommandHandler("delete", delete_handler))
    app.add_handler(CommandHandler("help", help_handler))
    app.add_handler(CommandHandler("get", get_handler))
    app.add_handler(CommandHandler("search", search_handler))
    app.add_handler(CommandHandler("edit", edit_handler))
    app.add_handler(CommandHandler("practice", practice_handler))
    app.add_handler(CommandHandler("stop_practice", stop_practice_handler))
    
    # Keep these MessageHandlers last to avoid interference with CommandHandlers
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, set_practice_mode))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, answer_handler))

    print("🤖 Bot is running...Press CTRL+C to stop.")
    app.run_polling() #This tells the bot to start listening for updates from Telegram. It uses polling, which means it keeps checking Telegram's server for new messages or commands.
   
 # ----------------------------------------------__name__ == "__main__"-------------------------------------------#

#It's a protective rule to: 
# Prevent the bot from starting when it shouldn't 
# Make your files safe to import in testing, unit tests, or future extensions
#in this case 
if __name__ == "__main__":
    main()
    