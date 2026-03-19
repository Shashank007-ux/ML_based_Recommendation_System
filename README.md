🚀 InternSaathi Backend - SIH 2025

InternSaathi is an AI-powered internship and placement platform designed to bridge the gap between students and campus placement cells. It features a microservices architecture with a Node.js Gateway and a Python ML Engine.

🌟 Key Features

Placement Prediction: Uses Gradient Boosting to predict a student's placement probability based on CGPA, Mock Scores, and Project history.

Smart Recommendations: Content-Based Filtering (TF-IDF) to recommend internships matching a student's skills and stipend requirements.

AI Resume Parser: Extracts skills, experience, and infers job roles from raw resume text (PDF/DOCX) using NLP and Naive Bayes classification.

Zero-Dependency: Runs entirely locally without external API keys (No OpenAI/Gemini required).

🏗️ Architecture

This project follows a Microservices pattern:

Node.js Gateway (Port 5000): Handles API routing and client communication.

Python ML Service (Port 8000): Exposes AI models via FastAPI.

🛠️ Setup Instructions

1. Prerequisites

Node.js (v18+)

Python (v3.9+)

PostgreSQL (Optional for DB features)

2. Setup ML Service (Python)

cd ml_service
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Create necessary folders
mkdir data models

# IMPORTANT: Place your CSV datasets in 'ml_service/data/'
# - comprehensive_students_data.csv
# - comprehensive_company_data.csv
# - UpdatedResumeDataSet.csv

# Train the models
python train_models.py

# Start the Server
uvicorn main:app --port 8000 --reload


3. Setup Gateway (Node.js)

cd node_server
npm install

# Create a .env file
echo "PORT=5000" > .env
echo "ML_SERVICE_URL=http://localhost:8000" >> .env
echo "DATABASE_URL=your_postgres_url" >> .env

# Start the Server
npm run dev


🧪 API Endpoints

Service

Method

Endpoint

Description

ML

POST

/parse-resume

Upload PDF/DOCX to extract skills & role

ML

POST

/predict-placement

Get placement probability score

ML

POST

/recommend-internships

Get matched internships based on profile

👥 Team AlgoNauts

Built for Smart India Hackathon 2025.
