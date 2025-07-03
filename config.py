"""
Configuration loader for Verint Migration Toolkit.

Loads sensitive credentials and base URL from a .env file to be used
for API authentication and data extraction.
"""

from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("VERINT_BASE_URL")
API_KEY_ID = os.getenv("VERINT_API_KEY_ID")
API_KEY_SECRET = os.getenv("VERINT_API_KEY_SECRET")