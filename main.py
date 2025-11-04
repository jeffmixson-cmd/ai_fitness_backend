from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from supabase import create_client, Client
import traceback

app = FastAPI()

# Supabase credentials
SUPABASE_URL = "https://brhqzfzfipwvlmxnqqod.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJyaHF6ZnpmaXB3dmxteG5xcW9kIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MTUyMzgyMywiZXhwIjoyMDc3MDk5ODIzfQ.6GCSDUtf1_-VXSBByA9_pV0Gooq5_GerFfY2UOsczBs"
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Models
class User(BaseModel):
    email: str
    display_name: str

class Workout(BaseModel):
    user_id: str
    name: str
    date: datetime  # Changed from date to datetime for compatibility

# Create user
@app.post("/users")
def create_user(user: User):
    try:
        data = {
            "email": user.email,
            "display_name": user.display_name
        }
        response = supabase.table("users").insert(data).execute()
        print("Supabase response:", response)
        return {"data": response.data}
    except Exception as e:
        print("Error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="User creation failed")

# Get users
@app.get("/users")
def get_users():
    try:
        response = supabase.table("users").select("*").execute()
        print("Supabase response:", response)
        return {"data": response.data}
    except Exception as e:
        print("Error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to fetch users")

# Create workout
@app.post("/workouts")
def create_workout(workout: Workout):
    try:
        data = {
            "user_id": workout.user_id,
            "name": workout.name,
            "date": workout.date.isoformat()
        }
        response = supabase.table("workouts").insert(data).execute()
        print("Supabase response:", response)
        return {"data": response.data}
    except Exception as e:
        print("Error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Workout creation failed")

# Get workouts
@app.get("/workouts")
def get_workouts():
    try:
        response = supabase.table("workouts").select("*").execute()
        print("Supabase response:", response)
        return {"data": response.data}
    except Exception as e:
        print("Error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail="Failed to fetch workouts")
