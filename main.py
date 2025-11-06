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

supabase = None

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
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Pydantic models -----
class User(BaseModel):
    email: str
    display_name: str

class Workout(BaseModel):
    user_id: str
    name: str
    date: datetime

class SupabaseResponse(BaseModel):
    data: List[Any]

# ----- Routes -----
@app.get("/")
def read_root():
    return {"message": "AI Fitness Backend is running"}

@app.get("/test")
def test_route():
    return {"status": "ok"}

@app.post("/users", response_model=SupabaseResponse)
def create_user(user: User):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client not initialized.")
    try:
        data = {"email": user.email, "display_name": user.display_name}
        response = supabase.table("users").insert(data).execute()
        logger.info(f"User created: {user.email}")
        return {"data": response.data}
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users", response_model=SupabaseResponse)
def get_users():
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client not initialized.")
    try:
        response = supabase.table("users").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workouts", response_model=SupabaseResponse)
def create_workout(workout: Workout):
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client not initialized.")
    try:
        data = {
            "user_id": workout.user_id,
            "name": workout.name,
            "date": workout.date.isoformat()
        }
        response = supabase.table("workouts").insert(data).execute()
        logger.info(f"Workout created: {workout.name}")
        return {"data": response.data}
    except Exception as e:
        logger.error(f"Error creating workout: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/workouts", response_model=SupabaseResponse)
def get_workouts():
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client not initialized.")
    try:
        response = supabase.table("workouts").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        logger.error(f"Error fetching workouts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/summary")
def get_summary():
    if not supabase:
        raise HTTPException(status_code=500, detail="Supabase client not initialized.")
    try:
        response = supabase.table("workouts").select("*").execute()
        workouts = response.data

        if not workouts:
            return {"summary": "No workouts found."}

        total_workouts = len(workouts)
        most_recent = max(workouts, key=lambda w: w["date"])
        names = [w["name"] for w in workouts if "name" in w]
        favorite = Counter(names).most_common(1)[0][0] if names else "N/A"

        return {
            "total_workouts": total_workouts,
            "most_recent_workout": {
                "name": most_recent.get("name", "Unknown"),
                "date": most_recent.get("date", "Unknown")
            },
            "favorite_workout_type": favorite
        }

    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
