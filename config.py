import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Google Gemini configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash"
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "models/gemini-embedding-001"
)

# Application configuration
APP_NAME = "DocuMind"
APP_DESCRIPTION = "Your AI-powered document assistant"

# Document processing configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval configuration
TOP_K = 4

# Storage configuration
DATA_DIR = "data"
VECTOR_STORE_DIR = "vector_store"

# API key validation
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY is missing. "
        "Please add your Gemini API key to the .env file."
    )