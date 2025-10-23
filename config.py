"""
Application configuration settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project path
BASE_DIR = Path(__file__).resolve().parent

# Database path
DB_DIR = BASE_DIR / "db"
DB_PATH = DB_DIR / "app_data.sqlite"

# API settings
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))

# Gemini API settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# RAG settings
MAX_RETRIEVAL_RESULTS = 5  # Maximum number of products returned from database

# Security settings
MAX_MESSAGE_LENGTH = 1000  # Maximum message length
RATE_LIMIT = "10/minute"  # Rate limit for requests

