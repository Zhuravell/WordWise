# Marks bot/ as a Python package.
# Makes sure that when you import from bot/, Python understands it's a package and not just a folder.

from bot.bot_core import main  # Making it easier to access 'main' when importing bot package
from bot.bot_commands import *  # Importing all commands from bot_commands.py (optional)