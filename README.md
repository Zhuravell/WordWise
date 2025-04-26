

python -m bot.bot_core     - to run a bot
-----------------DESCRIPTION-----------------------

WiseWord Bot

A Personal Own Vocabulary Storafe and Repetition System Telegram Bot for learning the Dutch Language.

Dutch Words, English Translation, Example(s), Dutch sentences using the target word, Comments, Source of the word learn, Category of the word (e.g. a specific topic or lexicon type).

Written in Python, with the help of SQLAlchemy.

Will implements rule-based and learning repetition models (DS/LM)

Will have Personal analytics as more words are learnt.

Will implement some visual aspects for interactive and visually appealing learning.


-----------------SET UP-----------------------------

Environment used for this bot: venv_WW_bot
source venv_WW_bot/bin/activate

Libraries:
pip install python-telegram-bot sqlalchemy psycopg2-binary python-dotenv

Models Folder - containe Backend and Database Management files.Do not run.
You should not run any file from the models folder, as they are automatically loaded when imported(by you, bot, other parts of a project). 


-----------------IMPLEMENTATION----------------------

For now, the development will be done and executed locally .Laptop will have to be on and connected to WiFi for a bot to work(even from a phone)
Later, it will be connected to a cloud service (e.g. AWS, Heroku) to run 24/7, without the laptop being turned on and connected.


------------------SOURCES--------------------

https://khashtamov.com/en/how-to-create-a-telegram-bot-using-python/ - an article on how to build a telegram bot with python
https://khashtamov.com/en/how-to-deploy-telegram-bot-django/ - an article on how to deploy a telegram bot with python
https://core.telegram.org/bots - Introduction to Telegram Bots
https://core.telegram.org/bots/api - Manual about Telegram Bots


