from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from supabase import create_client, Client
import os
import logging
from dotenv import load_dotenv

# ----- Load environment variables -----
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Missing Supabase environment variables. Please set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY.")

# ----- Initialize Supabase client -----
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ----- Configure logging -----
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ----- Initialize FastAPI app -----
app = FastAPI()

# ----- Add CORS middleware -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ✅ Replace with your frontend URL in production (e.g. https://myapp.vercel.app)
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
    date: date

# ----- Routes -----
@app.get("/")
def read_root():
    """Health check route"""
    return {"message": "AI Fitness Backend is running"}

@app.post("/users")
def create_user(user: User):
    """Create a new user"""
    try:
        data = {"email": user.email, "display_name": user.display_name}
        response = supabase.table("users").insert(data).execute()
        logger.info(f"User created: {user.email}")
        return {"data": response.data}
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users")
def get_users():
    """Retrieve all users"""
    try:
        response = supabase.table("users").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        logger.error(f"Error fetching users: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/workouts")
def create_workout(workout: Workout):
    """Create a new workout"""
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

@app.get("/workouts")
def get_workouts():
    """Retrieve all workouts"""
    try:
        response = supabase.table("workouts").select("*").execute()
        return {"data": response.data}
    except Exception as e:
        logger.error(f"Error fetching workouts: {e}")
        raise HTTPException(status_code=500, detail=str(e))
