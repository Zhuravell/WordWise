#Write basic functions to insert, query, update, and delete vocabulary entries from the database.
#These functions are then called by your bot commands.

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler
from models.db_setup import Session
from models.schema import DutchEnglishVocab
from bot.parsers import parse_add_command #, parse_edit_command
import random

    
#async def start_handler(update, context):
#    print("Hello learne, welcome to WordWise! Enjoy!") #pass  # Does nothing, but avoids the ImportError
# -------------------------------------------------Logic for /add command---------------------------------------------------#

async def add_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): #update - telegram object object,  context - CallbackContext object
    session = Session() #temporary connection with database, like opening and accesing specific sections of it for the duration of dealing with handlers, and then closing it.

    # Check for proper use of /add command
    if not context.args: #a guard caluse, checking if user made any input after calling /add command.if not, bot stops and shows how to use this command
        await update.message.reply_text( 
            "⚠️ Usage of /add command :\n`/add dutch_word | english_translation | [source] | [comment] | [example_sentence]`",
            parse_mode="Markdown" #just a stylistic element
        )
        return # Return acts like an anchor: it stops the function and any following code if no input is given after /add.

    # Join everything after /add and split by |
    input_str = ' '.join(context.args)    #now input_str = "ingewikkeld | complicated | Flikken | tricky situation" context.args is a list of all the units from the raw text
    
    user_dutch_word, user_english_word, user_source, user_comment, user_example_sentence = parse_add_command(input_str)
    # this is called unpacking of tuple into seperable variables ,remind you this is the tuple example from function call ("ingewikkeld", "complicated", "Flikken", "tricky case", "De situatie is ingewikkeld.")
    
    # Check for writing both dutch and english parts
    if not user_dutch_word or not user_english_word:
        await update.message.reply_text("❗ Please provide at least a Dutch word and and English transaltion")
        return
   
    # Check for duplicates
    existing = session.query(DutchEnglishVocab).filter_by(dutch_word=user_dutch_word).first()
    if existing:
        await update.message.reply_text(f"⚠️ The word '{user_dutch_word}' already exists in your list.")
        session.close()
        return

    # Create a new word entry, which will be literally a new row in posgresql table, and it is a python object representing a row
    new_entry = DutchEnglishVocab(
        dutch_word=user_dutch_word,
        english_word=user_english_word,
        source=user_source,
        comment=user_comment,
        example_sentence=user_example_sentence
    )
    #left side is PostgreSQL fields/ columns names, right side is input variables

    session.add(new_entry)
    session.commit()
    session.close()

    await update.message.reply_text(
    f"✅ Word '{user_dutch_word}' added!\nEnglish: {user_english_word}\nSource: {user_source or 'N/A'}\nComment: {user_comment or 'N/A'}\nExample: {user_example_sentence or 'N/A'}"
)


# ---------------------------------------------Logic for /list command--------------------------------------------#

async def list_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    words = session.query(DutchEnglishVocab).order_by(DutchEnglishVocab.id_word).all() #so words is a list of all words from DutchEnglishVocab table
    session.close()

    if not words: #if the list is empy, so if no words were found
        await update.message.reply_text("📭 Your word list is empty. Use /add to get started!")
        return

    # Format the words into a string
    word_list = "\n".join([ #step 3 Join all strings into one big string
        f"📌 *{word.dutch_word}* → _{word.english_word}_" # step 2 create each string, asterisk *...* make the word bold, underscores _..._ italic
        for word in words    #step 1 iterating over the words, which is a list of objects representing rows
    ])

    # Telegram messages have a max length (~4096 characters), so break into chunks if needed
    chunks = [word_list[i:i+4000] for i in range(0, len(word_list), 4000)]

    for chunk in chunks:
        await update.message.reply_text(chunk, parse_mode='Markdown')


#------------------------------------------------------Logic for /delete command--------------------------------------------------------#

async def delete_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()

    if not context.args:
        await update.message.reply_text("❗ Usage: /delete dutch_word")
        return

    word_to_delete = ' '.join(context.args).strip()
    word_entry = session.query(DutchEnglishVocab).filter_by(dutch_word=word_to_delete).first()

    if not word_entry:
        await update.message.reply_text(f"❌ The word '{word_to_delete}' was not found in your list.")
        session.close()
        return

    session.delete(word_entry)
    session.commit()
    session.close()
    
    #creating confirmation buttons
    keyboard = [
        [
            InlineKeyboardButton("✅ Yes, delete",callback_data = f"confirm_delete:{word_to_delete}"),
            InlineKeyboardButton("❌No, do not delete",callback_data = "cancel_delete")

        ]
    ]
    reply_markup =InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"⚠️Are you sure you would like to delete *{word_to_delete}*?", 
        parse_mode = "Markdown", 
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("confirm_delete:"):
        word_to_delete = query.data.split(":")[1]
        session = Session()
        
        word_entry = session.query(DutchEnglishVocab).filter_by(dutch_word = word_to_delete).first()
        
        if word_entry:
            session.delete(word_entry)
            session.commit()
            await query.edit_message_text(f"✅ Succesfully deleted *{word_to_delete}*.", parse_mode="Markdown")
        else:
            await query.edit_message_text(f"⚠️Word '{word_to_delete}' was not found.", parse_mode ="Markdown")
        
        session.close()
        
    elif query.data == "cancel_delete":
        await query.edit_message_text(text = "❌ Deletion canceled.")


    #await update.message.reply_text(f"🗑️ Deleted: *{word_to_delete}*", parse_mode="Markdown") 
    #instead of just a dutch word actually show the whole deleted row info


#------------------------------------------------------Logic for /help command--------------------------------------------------------#

async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "📚 *WordWise Bot Help*\n\n"
        "Here are the available commands:\n"
        "`/add dutch | english | [source] | [comment] | [example]` – Add a new word\n"
        "`/list` – List all added words\n"
        "`/get dutch_word` – View details of a word\n"
        "`/edit dutch_word | field | new_value` – Edit a field of a word\n"
        "`/delete dutch_word` – Delete a word\n"
        "`/search query` – Search for words containing a phrase\n"
        "`/help` – Show this help message"
    )
    await update.message.reply_text(help_text, parse_mode="Markdown")
     
        
#------------------------------------------------------Logic for /get command--------------------------------------------------------#
async def get_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    
    if not context.args:
        await update.message.reply_text("❗ Usage: /get dutch_word")
        return

    search_word = ' '.join(context.args).strip()
    word_entry = session.query(DutchEnglishVocab).filter_by(dutch_word=search_word).first()
    session.close()

    if not word_entry:
        await update.message.reply_text(f"🔍 The word '{search_word}' was not found.")
        return

    details = (
        f"📘 *{word_entry.dutch_word}* → _{word_entry.english_word}_\n"
        f"• Source: {word_entry.source or '—'}\n"
        f"• Comment: {word_entry.comment or '—'}\n"
        f"• Example: {word_entry.example_sentence or '—'}"
        )
    await update.message.reply_text(details, parse_mode="Markdown")

 
#------------------------------------------------------Logic for /search command--------------------------------------------------------#
async def search_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()

    if not context.args:
        await update.message.reply_text("❗ Usage: /search keyword")
        return

    query = ' '.join(context.args).strip().lower()

    results = session.query(DutchEnglishVocab).filter(
        DutchEnglishVocab.dutch_word.ilike(f"%{query}%") |
        DutchEnglishVocab.english_word.ilike(f"%{query}%")
        ).all()

    session.close()

    if not results:
        await update.message.reply_text("🔍 No matching words found.")
        return

    message = "\n".join([ f"🔹 *{word.dutch_word}* → _{word.english_word}_" for word in results])
    await update.message.reply_text(message, parse_mode="Markdown")
    
    
 #------------------------------------------------------Logic for /edit command--------------------------------------------------------#
async def edit_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()

    if not context.args or len(context.args) < 3:
        await update.message.reply_text("❗ Usage: /edit dutch_word | field | new_value")
        session.close()
        return

    input_str = ' '.join(context.args)
    parts = [part.strip() for part in input_str.split('|')]

    if len(parts) < 3:
        await update.message.reply_text("❗ Please use the format: /edit dutch_word | field | new_value")
        session.close()
        return

    word_to_edit = parts[0]
    field_to_edit = parts[1].lower()
    new_value = parts[2]

    word_entry = session.query(DutchEnglishVocab).filter_by(dutch_word=word_to_edit).first()

    if not word_entry:
        await update.message.reply_text(f"❌ The word '{word_to_edit}' was not found.")
        session.close()
        return

    valid_fields = ["dutch_word", "english_word", "source", "comment", "example_sentence"]
    if field_to_edit not in valid_fields:
        session.close()
        await update.message.reply_text("⚠️ Invalid field. Valid fields are: english_word, source, comment, example_sentence")
        return

    setattr(word_entry, field_to_edit, new_value) #Accessing and Modifying the Temporary Row Object with setattr(), int he temporary storage place in RAM, where word_entry is stored
    session.commit()
    session.close()

    await update.message.reply_text(f"✏️ Updated {word_to_edit} – {field_to_edit} changed to: {new_value}")


 
 
 
 
# ------------------------------------------------------------------------ PRACTICE --------------------------------------------------------------#


 #----------------------------------------------------------------------practice_handler--------------------------------------------------------------#

async def practice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Great, lets start practicing.\n"
        "Please choose your practice mode:\n"
        "1. Dutch to English (Type: dutch_to_english)\n"
        "2. English to Dutch (Type: english_to_dutch)\n"
        "3. Mixed Mode (Type: mixed)")
    context.user_data.clear()  # Reset previous practice session if it exists
    

# ---------------------------------------------------------------------set_practice_mode ----------------------------------------------------------------#

async def set_practice_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip().lower()

    if user_input not in ["dutch_to_english", "english_to_dutch", "mixed"]:
        await update.message.reply_text("❗ Invalid mode. Please choose: dutch_to_english, english_to_dutch, or mixed.")
        return
    
    context.user_data.clear()  # Reset previous practice session
    context.user_data["mode"] = user_input
    context.user_data["score"] = 0
    context.user_data["total_questions"] = 0

    await update.message.reply_text(f"✅ Mode set to {user_input}. Let's begin the practice session!")
    await next_question(update, context)
    
    
# ---------------------------------------------------------------------next_question ----------------------------------------------------------------#

async def next_question(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    words = session.query(DutchEnglishVocab).all()

    if not words:
        await update.message.reply_text("📭 Your vocabulary list is empty. Add some words to start practicing!")
        session.close()
        return

    word_entry = random.choice(words)
    mode = context.user_data["mode"]

    context.user_data["current_word_id"] = word_entry.id_word

    if mode == "dutch_to_english":
        context.user_data["question_type"] = "dutch_to_english"
        await update.message.reply_text(f"Translate this word to English: *{word_entry.dutch_word}*", parse_mode="Markdown")
    elif mode == "english_to_dutch":
        context.user_data["question_type"] = "english_to_dutch"
        await update.message.reply_text(f"Translate this word to Dutch: *{word_entry.english_word}*", parse_mode="Markdown")
    else: #Mixed Mode
        if random.choice([True, False]):
            context.user_data["question_type"] = "dutch_to_english"
            await update.message.reply_text(f"Translate this word to English: *{word_entry.dutch_word}*", parse_mode="Markdown")
        else:
            context.user_data["question_type"] = "english_to_dutch"
            await update.message.reply_text(f"Translate this word to Dutch: *{word_entry.english_word}*", parse_mode="Markdown")
    
    session.close()  # Close session after use.
            
#--------------------------------------------------------------------------answer_handler--------------------------------------------#

async def answer_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    session = Session()
    user_answer = update.message.text.strip().lower()
    word_id = context.user_data["current_word_id"]
    mode = context.user_data["mode"]
    question_type = context.user_data.get("question_type")
    
    if not word_id:
        await update.message.reply_text("❗ Error: No word is currently being practiced.")
        session.close()
        return

    word_entry = session.query(DutchEnglishVocab).filter_by(id=word_id).first()
    session.close()

    if question_type == "dutch_to_english":
        correct_answer = word_entry.english_word.lower()
    elif question_type == "english_to_dutch":
        correct_answer = word_entry.dutch_word.lower()    
    
    context.user_data["total_questions"] += 1
    
    if user_answer == correct_answer:
        context.user_data["score"] += 1
        await update.message.reply_text("✅ Correct!")
    else:
        await update.message.reply_text(f"❌ Incorrect. The correct answer is: *{correct_answer}*.", parse_mode="Markdown")
    
    await next_question(update, context)


#-------------------------------------------------------------stop_practice_handler---------------------------------------------------#

async def stop_practice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    score = context.user_data.get("score", 0)
    total = context.user_data.get("total_questions", 0)
    
    if total == 0:
        await update.message.reply_text("🛑 You haven't answered any questions yet.")
    else:
        accuracy = (score / total) * 100
        await update.message.reply_text(
            f"🛑 Practice session ended.\n"
            f"Total questions: {total}\n"
            f"Correct answers: {score}\n"
            f"Accuracy: {accuracy:.2f}%")
    context.user_data.clear()

print("✅ bot_commands.py loaded successfully and handlers are defined.")  # Add this line for debugging


#--------------------------------------------------------------------------------------------------------------------------------------#







#python -m bot.bot_core 



#context.args - is list of strings including all the elements (namely arguments) the user input after the command.It splits input by spaces
#example
# user input : /edit ingewikkeld | complex | It's a difficult word.
# user.message.text: "/edit ingewikkeld | complex | It's a difficult word."
# context.args: ['ingewikkeld', '|', 'complex', '|', "It's", 'a', 'difficult', 'word.']

#✅ context.user_data is a predefined storage mechanism, but the data you store in it (like score, index, etc.) is entirely created by you. 
