from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity

# --- APP CONFIGURATION ---
app = FastAPI(title="InternSaathi ML Engine", version="1.0")

# Paths to the saved models (from the previous step)
MODELS_PATH = "models"
PLACEMENT_MODEL_FILE = os.path.join(MODELS_PATH, "placement_model.pkl")
VECTORIZER_FILE = os.path.join(MODELS_PATH, "tfidf_vectorizer.pkl")
MATRIX_FILE = os.path.join(MODELS_PATH, "tfidf_matrix.pkl")
METADATA_FILE = os.path.join(MODELS_PATH, "internships_metadata.pkl")

# --- STATIC FILES ---
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# --- GLOBAL VARIABLES TO HOLD MODELS ---
# We load these once on startup to make the API fast
models = {}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def load_models():
    """Load all ML models into memory when server starts."""
    try:
        models["placement_clf"] = joblib.load(PLACEMENT_MODEL_FILE)
        models["vectorizer"] = joblib.load(VECTORIZER_FILE)
        models["tfidf_matrix"] = joblib.load(MATRIX_FILE)
        models["internships_df"] = joblib.load(METADATA_FILE)
        print("All ML Models loaded successfully!")
    except FileNotFoundError as e:
        print(f"Error loading models: {e}")
        print("Did you run 'train_models.py' first?")

# --- INPUT DATA MODELS (Pydantic) ---
# These define the JSON structure the frontend must send

class StudentStats(BaseModel):
    CGPA: float
    Mock_OA_Score: int
    Projects: int
    Internships_Done: int

class StudentProfile(BaseModel):
    Skills: str       # e.g., "Python, React, SQL"
    Preferred_Role: str # e.g., "Data Scientist"
    Location: str     # e.g., "Bangalore" (Optional)

# --- API ENDPOINTS ---

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/predict")
def predict_page():
    return FileResponse("static/predict.html")

@app.get("/recommend")
def recommend_page():
    return FileResponse("static/recommend.html")

@app.post("/predict-placement")
def predict_placement(student: StudentStats):
    """
    Predicts if a student is at risk of not being placed.
    """
    if "placement_clf" not in models:
        raise HTTPException(status_code=500, detail="Model not loaded")

    # 1. Prepare Input Data (Must match training columns exactly)
    # Feature order: ['CGPA', 'Mock_OA_Score', 'Projects', 'Internships_Done']
    input_df = pd.DataFrame([student.dict()])
    
    # 2. Make Prediction
    clf = models["placement_clf"]
    
    # Get probability (e.g., [0.2, 0.8] -> 80% chance of placement)
    # class 0 = Not Placed, class 1 = Placed
    probs = clf.predict_proba(input_df)[0] 
    success_probability = round(probs[1] * 100, 2)
    
    # Determine Status
    status = "Safe" if success_probability > 65 else "At Risk"

    # --- Generate Detailed Analytics ---
    feedback = []
    
    # CGPA Analysis
    if student.CGPA >= 8.5:
        feedback.append("Excellent Academic Record: Your CGPA is a strong asset.")
    elif student.CGPA >= 7.0:
        feedback.append("Good Academic Standing: Your CGPA is decent, but pushing it to 8.0+ would be beneficial.")
    else:
        feedback.append("Academic Focus Needed: A CGPA below 7.0 can be a hurdle. Focus on improving your grades.")

    # OA Score Analysis
    if student.Mock_OA_Score >= 80:
        feedback.append("Strong Problem Solving: High Mock OA score indicates good DSA preparation.")
    elif student.Mock_OA_Score >= 60:
        feedback.append("Average OA Performance: Consistent practice is needed to cross the 80+ mark.")
    else:
        feedback.append("Critical Area - OA: Your OA score is low. heavy focus on LeetCode/DSA is strictly recommended.")

    # Projects & Internships
    if student.Projects >= 3:
        feedback.append("Strong Portfolio: Good number of projects showcased.")
    elif student.Projects < 2:
        feedback.append("Portfolio Gap: You have very few projects. Build 1-2 robust full-stack or ML projects.")

    if student.Internships_Done == 0:
        feedback.append("Experience Gap: Zero internships can be a red flag. Look for startups or open source contributions.")
    
    return {
        "placement_probability": success_probability,
        "status": status,
        "message": "High chance of placement" if status == "Safe" else "Needs Mentorship",
        "analysis": feedback
    }

@app.post("/recommend-internships")
def recommend_internships(profile: StudentProfile):
    """
    Returns top 5 internships based on skills and preferences.
    """
    if "vectorizer" not in models:
        raise HTTPException(status_code=500, detail="Models not loaded")

    # 1. Create Query String
    # Combine user inputs into one text string to match our training logic
    query_text = f"{profile.Preferred_Role} {profile.Skills} {profile.Location}"
    
    # 2. Vectorize Query
    vectorizer = models["vectorizer"]
    tfidf_matrix = models["tfidf_matrix"]
    
    query_vector = vectorizer.transform([query_text])
    
    # 3. Calculate Similarity
    cosine_scores = cosine_similarity(query_vector, tfidf_matrix)
    
    # 4. Rank Results
    # Get scores as list, sort descending
    score_pairs = list(enumerate(cosine_scores[0]))
    sorted_scores = sorted(score_pairs, key=lambda x: x[1], reverse=True)
    
    # Get Top 5 indices
    top_indices = [i[0] for i in sorted_scores[:5]]
    
    # 5. Fetch Internship Details
    df = models["internships_df"]
    recommendations = df.iloc[top_indices][['Internship_ID', 'Company', 'Role', 'Location', 'Stipend', 'Required_Skills']]
    
    # Convert to JSON format
    return recommendations.to_dict(orient="records")