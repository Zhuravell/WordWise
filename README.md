# WordWise
WordWise (WW) is a telegram bot used for storage and practice of Dutch vocabulary. 

## User Manual
- in order to start a bot run the following line in the terminal:  python -m bot.bot_core
- in order to stop a bot press following keyboard buttons:  CTRL C





## bot/ Package Overview

This package contains the main logic for the WordWise Telegram bot.

- `__init__.py`: Declares the package and summarizes structure.
- `bot_core.py`: Initializes the bot, sets up the dispatcher, and registers all command handlers.
- `bot_commands.py`: Contains command and message handlers (currently ~8), including vocabulary management and user interaction.
- `parsers.py`: Helper functions for parsing input/output, formatting messages, etc.
- `utils.py`: Reserved for general-purpose utilities (currently empty).

Highlights:
- Implements core bot commands for adding, retrieving, editing, and managing vocabulary.
- Integrates a practice session feature: the bot quizzes users with words from their own vocabulary list and checks their responses.





## models/ Package Overview

This package contains the database layer of the WordWise bot, implemented using SQLAlchemy.
Uses PostgreSQL as the database backend. Connection details are managed via `.env` and loaded with `python-dotenv`.

- `__init__.py`: Exposes `Session`, `Base`, and the model class for easy importing elsewhere in the project.
- `db_setup.py`: Configures the database engine and session factory. Provides `init_db()` to create all tables.
- `schema.py`: Defines the data model `DutchEnglishVocab` and the declarative base `Base`.

Usage:
- Do not run files directly, except `db_setup.py` if initializing the database.
- Other modules should import `Session` and models from `models` to interact with the database.



## Purpose
This bot assists with vocabulary retention and active recall as part of my self-study for the Dutch B1 Staatsexamen(Programma I).
