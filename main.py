from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Any
from collections import Counter
import os
import logging
from dotenv import load_dotenv

# ----- Configure logging -----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----- Load environment variables -----
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

supabase = None  # Default to None

# ----- Initialize Supabase client -----
try:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Missing Supabase environment variables.")
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    logger.info("✅ Supabase client initialized successfully.")
except Exception as e:
    logger.warning(f"⚠️ Supabase client not initialized: {e}")
    supabase = None

# ----- Initialize FastAPI app -----
app = FastAPI()

# ----- Add CORS middleware -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],