# ResumeRank — Automated Resume Ranking System

AI-powered resume ranking using NLP, TF-IDF, and weighted scoring.

## Project Structure

```
resume_ranker/
├── app.py               ← Flask web server
├── ranker.py            ← ML ranking logic (TF-IDF + weighted scoring)
├── skills_database.py   ← Master skills list (7 categories)
├── requirements.txt     ← Dependencies
├── Resume.csv           ← Kaggle dataset (place here)
└── templates/
    └── index.html       ← Full UI (Resume Ranking + Gap Analysis)
```

## Setup & Run

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Place Kaggle dataset
# Download from: https://www.kaggle.com/datasets/snehaanbhawal/resume-dataset
# Place Resume.csv in this folder

# 3. Run the app
python app.py

# 4. Open browser
# Go to: http://localhost:5000
```

## Features

### Resume Ranking Tab
- Paste any job description
- Filter by job category
- Control top N results
- Ranks candidates using 5 weighted factors:
  - Skill Match (40%)
  - TF-IDF Cosine Similarity (25%)
  - Experience Score (20%)
  - Education Score (10%)
  - Keyword Density (5%)
- Shows matched/missing skills per candidate
- Score breakdown bars per candidate

### Gap Analysis Tab
- Paste any resume + job description
- Get full skills gap report
- Matched, missing, and bonus skills
- Visual donut chart with match %
- Category-wise breakdown

## Tech Stack
- Python, Flask
- Scikit-learn (TF-IDF, Cosine Similarity)
- NLP (regex-based skill extraction)
- Pandas, NumPy
