from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("VERINT_BASE_URL")
API_KEY_ID = os.getenv("VERINT_API_KEY_ID")
API_KEY_SECRET = os.getenv("VERINT_API_KEY_SECRET")