from collections import Counter

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

        # Most recent workout by date
        most_recent = max(workouts, key=lambda w: w["date"])

        # Most common workout name
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
