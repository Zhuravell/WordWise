# Handles database connection & Defines and manages a Session to interact with the database.
# Indirectly accessed by other files to interact with the database.
# Provides a init_db() function to initialize the database.

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.schema import Base, DutchEnglishVocab
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("⚠️ DATABASE_URL is not set in the .env file.")

engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)  # Creates all tables defined in your models

if __name__ == "__main__":
    init_db()
    print("✅ Database initialized successfully!")



# sessionmaker(bind=engine)    # Factory that builds custom Session classes (Audi Factory)
# Session                      # Class / blueprint of how to connect to the database (Audi design manual)
# Session()                    # Call to build a usable connection (Build a car)
# session                      # Actual live connection to the DB (Drive the car temporarily)

#session = Session()           # Start the connection (get in the car)
#session.add(...)              # Queue a change (load cargo)
#session.commit()              # Save changes (deliver cargo)
#session.close()               # End the session (park the car)




