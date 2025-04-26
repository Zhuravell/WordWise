
# One-time script during intiial setup to create database tables, or can be run when updating table structure 


from sqlalchemy import create_engine
from models.schema import Base  # Adjusted import
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Get database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if the database URL is correctly loaded
if not DATABASE_URL:
    raise ValueError("⚠️ DATABASE_URL is not set in the .env file.")

# Connect and create tables
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

print("✅ Tables created successfully!")











