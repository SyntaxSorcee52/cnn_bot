import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

faculties = [
    "Мехмат", "ФПМИ", "Химфак", "Физфак",
    "Юрфак", "Эконом", "Журфак", "Истфак"
]