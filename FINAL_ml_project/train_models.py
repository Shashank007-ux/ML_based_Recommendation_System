import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import os

# --- CONFIGURATION ---
DATA_PATH = "data"
MODELS_PATH = "models"
STUDENT_FILE = "comprehensive_students_data.csv" 
INTERNSHIP_FILE = "comprehensive_company_data.csv"

# Ensure models directory exists
os.makedirs(MODELS_PATH, exist_ok=True)

def train_placement_model():
    print("\n--- Training Placement Prediction Model ---")
    
    # 1. Load Data
    df = pd.read_csv(os.path.join(DATA_PATH, STUDENT_FILE))
    
    # 2. Select Features (X) and Target (y)
    # We use academic stats + project counts. 
    # Note: We are ignoring 'Skills' text for this specific numeric model to keep it simple and fast.
    features = ['CGPA', 'Mock_OA_Score', 'Projects', 'Internships_Done']
    target = 'Placed_Status'
    
    X = df[features]
    y = df[target]
    
    # 3. Split Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 4. Train Model (Random Forest)
    # increased estimators for smoother probability curves
    # max_depth=10 to prevent overfitting to noise (less drastic jumps)
    clf = RandomForestClassifier(n_estimators=300, max_depth=10, min_samples_leaf=5, random_state=42)
    clf.fit(X_train, y_train)
    
    # 5. Evaluate
    y_pred = clf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # 6. Save Model
    joblib.dump(clf, os.path.join(MODELS_PATH, 'placement_model.pkl'))
    print(f"Saved placement model to {MODELS_PATH}/placement_model.pkl")


def train_recommendation_engine():
    print("\n--- Building Internship Recommendation Engine ---")
    
    # 1. Load Data
    df = pd.read_csv(os.path.join(DATA_PATH, INTERNSHIP_FILE))
    
    # 2. Preprocessing
    # We create a single 'tags' column that contains all important keywords
    # This helps the model match a query like "Python in Bangalore" 
    df['tags'] = df['Role'] + " " + \
                 df['Required_Skills'] + " " + \
                 df['Location'] + " " + \
                 df['Company'] + " " + \
                 df['Description']
                 
    # Fill NaN values just in case
    df['tags'] = df['tags'].fillna('')
    
    # 3. Vectorization (TF-IDF)
    # Convert text to numbers
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(df['tags'])
    
    # 4. Save Artifacts
    # We need 3 things to run the API:
    # A) The Vectorizer (to convert User Input -> Numbers)
    # B) The Matrix (The "Database" of pre-calculated internship vectors)
    # C) The DataFrame (To return the actual details like 'Company Name' to the user)
    
    joblib.dump(tfidf, os.path.join(MODELS_PATH, 'tfidf_vectorizer.pkl'))
    joblib.dump(tfidf_matrix, os.path.join(MODELS_PATH, 'tfidf_matrix.pkl'))
    joblib.dump(df, os.path.join(MODELS_PATH, 'internships_metadata.pkl'))
    
    print(f"Saved Vectorizer, Matrix, and Metadata to {MODELS_PATH}/")

if __name__ == "__main__":
    # Check if data exists
    if not os.path.exists(os.path.join(DATA_PATH, STUDENT_FILE)):
        print(f"ERROR: File {STUDENT_FILE} not found in {DATA_PATH}/ folder.")
        print("Please generate the data first and save it there.")
    else:
        train_placement_model()
        train_recommendation_engine()
        print("\nAll training complete! Ready for API integration.")