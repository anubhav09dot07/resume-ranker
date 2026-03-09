from flask import Flask, render_template, request, jsonify
import pandas as pd
from pathlib import Path
from ranker import rank_resumes, analyze_gap, extract_skills_detailed

# Use Flask's default templates/ directory for deployment compatibility.
app = Flask(__name__)

# Load dataset once at startup
BASE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BASE_DIR.parent
DATA_CANDIDATES = [
    PROJECT_ROOT / 'data' / 'Resume.csv',
    PROJECT_ROOT / 'Resume.csv',
    BASE_DIR / 'Resume.csv',
]
df = None

def load_data():
    global df
    data_path = next((p for p in DATA_CANDIDATES if p.exists()), None)

    if data_path is not None:
        df = pd.read_csv(data_path)

        # Normalize expected resume column name across different datasets.
        if 'Resume' not in df.columns and 'Resume_str' in df.columns:
            df = df.rename(columns={'Resume_str': 'Resume'})
        if 'Resume' not in df.columns:
            raise ValueError("Dataset must contain either 'Resume' or 'Resume_str' column.")

        if 'Category' not in df.columns:
            df['Category'] = 'Unknown'

        df['Resume'] = df['Resume'].fillna('').astype(str)
        df['Category'] = df['Category'].fillna('Unknown').astype(str)
        print(f"✅ Loaded {len(df)} resumes from {data_path}")
        return

    print("⚠️  Resume.csv not found. Using sample data.")
    df = pd.DataFrame({
        'Category': ['Data Science', 'Python Developer', 'Java Developer',
                     'Data Science', 'Machine Learning'] * 10,
        'Resume': [
            'Python developer with 5 years experience in machine learning tensorflow keras scikit-learn sql aws docker',
            'Experienced python django flask developer with 3 years REST API postgresql redis git',
            'Java spring boot developer 4 years experience microservices kubernetes docker aws jenkins',
            'Data scientist with deep learning nlp pytorch tensorflow 2 years experience bachelors degree',
            'Machine learning engineer 6 years python tensorflow pytorch aws kubernetes phd computer science'
        ] * 10
    })

load_data()

@app.route('/')
def index():
    categories = ['All'] + sorted(df['Category'].unique().tolist())
    stats = {
        'total_resumes': len(df),
        'total_categories': df['Category'].nunique(),
        'top_category': df['Category'].value_counts().index[0],
    }
    return render_template('index.html', categories=categories, stats=stats)


@app.route('/rank', methods=['POST'])
def rank():
    data = request.get_json()
    jd = data.get('job_description', '')
    category = data.get('category', 'All')
    top_n = int(data.get('top_n', 10))

    if not jd.strip():
        return jsonify({'error': 'Job description is required'}), 400

    results_df = rank_resumes(df, jd, top_n=top_n, category=category)

    if results_df.empty:
        return jsonify({'error': 'No resumes found for this category'}), 404

    results = results_df.to_dict(orient='records')
    return jsonify({'results': results, 'total': len(results)})


@app.route('/gap_analysis', methods=['POST'])
def gap_analysis():
    data = request.get_json()
    resume_text = data.get('resume_text', '')
    jd_text = data.get('jd_text', '')

    if not resume_text or not jd_text:
        return jsonify({'error': 'Both resume and JD are required'}), 400

    gap = analyze_gap(resume_text, jd_text)
    category_skills = extract_skills_detailed(resume_text)
    jd_skills = extract_skills_detailed(jd_text)

    return jsonify({
        'gap': gap,
        'resume_categories': category_skills,
        'jd_categories': jd_skills
    })


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
