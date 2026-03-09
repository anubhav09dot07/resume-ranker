# 🎯 AI-Powered Resume Ranking System

An intelligent resume screening system that uses machine learning, NLP, and weighted scoring algorithms to match job descriptions with candidate resumes. Features automated skill extraction, gap analysis, and visual score reports.

[![Live Demo](https://img.shields.io/badge/Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/anubhav0907/resume-ranker)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/anubhav09dot07/resume-ranker)

---

## 🚀 Key Features

- **Multi-Factor Ranking**: Combines 5 weighted scoring components for accurate candidate evaluation
- **Intelligent Skill Extraction**: Regex + NLP-based matching across 7 technical categories (100+ skills)
- **Skill Gap Analysis**: Identifies matched, missing, and bonus skills for each candidate
- **Category Filtering**: Supports 25 job categories with 2,484+ resumes
- **Interactive Web UI**: Real-time ranking with visual score breakdowns and donut charts
- **Export Results**: Download ranked candidates and gap analysis reports as CSV
- **Minimal Modern Design**: Clean interface with Helvetica typography and responsive layout

---

## 🧠 Machine Learning Models

### Model 1: Resume Classification
Predicts which of 25 job categories a resume belongs to using TF-IDF vectorization and multiple classifiers.

| Model | Accuracy | Status |
|-------|----------|--------|
| **Random Forest** | **74.04%** | ✅ Best |
| Linear SVM | 72.84% | |
| Logistic Regression | 69.82% | |
| Naive Bayes | 57.75% | |
| KNN | 55.33% | |

- **Dataset**: 2,484 resumes across 25 categories
- **Train/Test Split**: 80/20 (1,987 / 497 samples)
- **Vectorization**: TF-IDF (10,000 features, 1-3 grams)
- **Preprocessing**: Lemmatization, stopword removal, lowercase

### Model 2: Weighted Ranking System
Multi-component scoring system for ranking resumes against specific job descriptions.

**Scoring Components**:
- 🎯 **Skill Match** (40%) - NLP-based skill extraction and matching
- 📊 **TF-IDF Similarity** (25%) - Cosine similarity between resume and JD
- 💼 **Experience Score** (20%) - Years of experience evaluation
- 🎓 **Education Score** (10%) - Degree level assessment
- 🔑 **Keyword Density** (5%) - Job description keyword overlap

---

## 🛠️ Tech Stack

### Backend
- **Python 3.11** - Core programming language
- **Flask 3.0.0** - Web framework & REST API
- **scikit-learn 1.3.0** - Machine learning algorithms
- **Pandas 2.1.0** - Data manipulation
- **NumPy 1.26.0** - Numerical computing
- **Gunicorn 21.2.0** - Production WSGI server

### Frontend
- **HTML5/CSS3** - Minimal, clean UI design
- **JavaScript** - Vanilla JS (no frameworks)
- **Responsive Design** - Mobile-first approach
- **Helvetica Font Stack** - Professional typography

### Deployment
- **Docker** - Containerization
- **Git** - Version control
- **Railway** - Platform deployment
- **Hugging Face Spaces** - Demo hosting

---

## 📁 Project Structure

```
resume_ranking/
├── Flask_web_app_UI/              # Production web application
│   ├── app.py                     # Flask server + API routes
│   ├── ranker.py                  # Core ranking algorithms
│   ├── skills_database.py         # Skills taxonomy (100+ skills)
│   ├── templates/
│   │   └── index.html             # Frontend UI
│   ├── requirements.txt           # Python dependencies
│   ├── Dockerfile                 # Container configuration
│   ├── Procfile                   # Railway deployment config
│   └── render.yaml                # Render.com deployment config
│
├── notebooks/                     # Jupyter analysis notebooks
│   ├── model1.ipynb              # Resume classification training
│   ├── model2.ipynb              # Weighted ranking system
│   ├── resume_EDA.ipynb          # Exploratory data analysis
│   ├── skill_extraction.ipynb    # NLP skill matching
│   ├── skillgapanalysis.ipynb    # Gap analysis algorithm
│   └── weightageranksys.ipynb    # Weighted scoring system
│
├── data/
│   ├── Resume.csv                # Main dataset (2,484 resumes)
│   ├── ranked_candidates.csv     # Output results
│   └── gap_analysis_results.csv  # Skill gap reports
│
├── models/                        # Saved ML models (joblib)
├── scripts/                       # Utility scripts
└── docs/                          # Documentation
```

---

## 🔧 Installation & Setup

### Prerequisites
- Python 3.11+
- pip package manager
- Virtual environment (recommended)

### Local Development

1. **Clone the repository**
```bash
git clone https://github.com/anubhav09dot07/resume-ranker.git
cd resume-ranker
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
cd Flask_web_app_UI
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the app**
Open your browser and navigate to `http://localhost:5000`

---

## 🚀 Deployment

### Railway Deployment
1. Connect GitHub repository to Railway
2. Railway auto-detects `Procfile`
3. Set environment variables (if needed)
4. Deploy with one click

### Hugging Face Spaces
1. Create new Space with Docker SDK
2. Clone the Space repository
3. Copy app files (exclude large CSV if >10MB)
4. Push to Space: `git push origin main`

### Docker Deployment
```bash
docker build -t resume-ranker .
docker run -p 7860:7860 resume-ranker
```

---

## 📡 API Reference

### POST /rank
Rank resumes against a job description.

**Request**:
```json
{
  "job_description": "Looking for Python developer with ML experience...",
  "category": "Data Science",  // Optional, default: "All"
  "top_n": 10                  // Optional, range: 5-20
}
```

**Response**:
```json
{
  "results": [
    {
      "rank": 1,
      "category": "Data Science",
      "skill_score": 85.5,
      "tfidf_score": 72.3,
      "exp_score": 100.0,
      "edu_score": 100.0,
      "keyword_score": 68.2,
      "final_score": 82.4,
      "matched_skills": ["python", "tensorflow", "sql"],
      "missing_skills": ["aws", "docker"],
      "bonus_skills": ["pytorch", "kubernetes"],
      "experience": "5 years",
      "education": "Masters",
      "fit_label": "Strong Fit"
    }
  ]
}
```

### POST /gap_analysis
Analyze skill gaps for a specific resume.

**Request**:
```json
{
  "job_description": "Looking for Python developer...",
  "resume_text": "Data scientist with 5 years experience..."
}
```

**Response**:
```json
{
  "match_percentage": 75.5,
  "matched_skills": ["python", "pandas", "sql"],
  "missing_skills": ["aws", "docker"],
  "bonus_skills": ["pytorch"],
  "category_breakdown": {
    "Programming Languages": {"matched": 3, "missing": 1},
    "ML & Data Science": {"matched": 2, "missing": 2}
  }
}
```

---

## 📊 Dataset Information

- **Source**: Kaggle Resume Dataset
- **Total Resumes**: 2,484
- **Categories**: 25 job types
- **Format**: CSV (Resume text + Category label)
- **File Size**: 53.66 MB

**Sample Categories**:
- Data Science (120 resumes)
- Python Developer (120 resumes)
- Java Developer (118 resumes)
- Web Development (115 resumes)
- Machine Learning (110 resumes)
- And 20 more...

---

## 🎯 Core Algorithms

### 1. Skill Extraction
- Regex pattern matching against 100+ skills database
- Word boundary detection for accuracy
- Category-wise grouping (7 categories)

### 2. TF-IDF Cosine Similarity
- Vectorizes resume and job description text
- Calculates semantic similarity (0-1 scale)
- Max 1,500 features, 1-2 grams

### 3. Experience Scoring
- Extracts years from patterns: "X years experience", "X+ yrs"
- Normalizes against job requirements
- Handles ranges and approximate values

### 4. Education Level Scoring
- Detects: PhD (4), Masters (3), Bachelors (2), Diploma (1)
- Keyword matching with synonyms
- Handles variations (MSc, BS, MBA, etc.)

### 5. Weighted Final Score
- Combines all 5 components with configurable weights
- Normalizes to 0-100 scale
- Provides fit labels:
  - **Strong Fit** (80-100%)
  - **Good Fit** (60-79%)
  - **Moderate Fit** (40-59%)
  - **Weak Fit** (0-39%)

---

## 🎨 UI Features

### Resume Ranking Tab
- Paste job description input
- Category filter dropdown (25 options)
- Top N results slider (5-20)
- Visual weight distribution
- Animated result cards with:
  - Rank badge (gold/silver/bronze)
  - Final score (0-100)
  - Component score breakdown (5 bars)
  - Matched skills (green chips)
  - Missing skills (red chips)
  - Experience & education tags
  - Resume preview (expandable)

### Gap Analysis Tab
- One-on-one comparison
- Donut chart visualization
- Skills breakdown by category
- Match percentage display
- Color-coded skill chips

---

## 🔮 Future Enhancements

- [ ] Deep learning models (BERT, GPT-based embeddings)
- [ ] Multi-language resume support
- [ ] PDF resume parsing and upload
- [ ] ATS (Applicant Tracking System) integration
- [ ] Candidate profile management dashboard
- [ ] Email notification system
- [ ] Advanced analytics and reporting
- [ ] Custom weight configuration UI
- [ ] Interview scheduling integration
- [ ] Mobile app version

---

## 📈 Performance Metrics

- **Resume Processing Speed**: ~50 resumes/second
- **API Response Time**: <500ms average
- **Skill Extraction Accuracy**: ~85% precision
- **Classification Accuracy**: 74.04% (Random Forest)
- **Concurrent Users**: Tested up to 10 simultaneous requests

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available for educational and commercial use.

---

## 👤 Author

**Anubhav Vyas**
- Email: 09anubhavvyas11@gmail.com
- GitHub: [@anubhav09dot07](https://github.com/anubhav09dot07)
- LinkedIn: [Add your LinkedIn profile]

---

## 🙏 Acknowledgments

- Kaggle for the resume dataset
- scikit-learn community for ML tools
- Flask framework contributors
- Hugging Face for deployment platform

---

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Email: 09anubhavvyas11@gmail.com

---

**⭐ Star this repository if you find it helpful!**
