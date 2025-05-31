# Marks models/ as a Python package. Makes importing models and session easier throughout the project.
# Never run directly. It's loaded automatically when you import from models/.

from models.schema import DutchEnglishVocab, Base  # Importing your Base and models here
from models.db_setup import Session  # Importing Session here for convenience

