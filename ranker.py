import re
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills_database import SKILLS_DB

WEIGHTS = {
    'skill_match':      0.40,
    'tfidf_similarity': 0.25,
    'experience':       0.20,
    'education':        0.10,
    'keyword_density':  0.05
}

EDU_KEYWORDS = {
    'phd':       ['phd', 'ph.d', 'doctorate'],
    'masters':   ['master', 'msc', 'mba', 'm.tech', 'ms'],
    'bachelors': ['bachelor', 'bsc', 'b.tech', 'b.e', 'be'],
    'diploma':   ['diploma', 'associate']
}
EDU_RANK = {'phd': 4, 'masters': 3, 'bachelors': 2, 'diploma': 1, 'none': 0}


def clean_text(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    return text.lower().strip()


def extract_skills_flat(text):
    text_lower = text.lower()
    found = set()
    for skills in SKILLS_DB.values():
        for skill in skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found.add(skill)
    return found


def extract_skills_detailed(text):
    text_lower = text.lower()
    found = {}
    for category, skills in SKILLS_DB.items():
        matched = []
        for skill in skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                matched.append(skill)
        if matched:
            found[category] = matched
    return found


def extract_years(text):
    patterns = [
        r'(\d+)\+?\s*years?\s*of\s*experience',
        r'(\d+)\+?\s*years?\s*experience',
        r'(\d+)\+?\s*yrs?\s*experience',
        r'experience\s*of\s*(\d+)\+?\s*years?',
    ]
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        years.extend([int(y) for y in matches])
    return max(years) if years else 0


def detect_education(text):
    text_lower = text.lower()
    for level, keywords in EDU_KEYWORDS.items():
        if any(k in text_lower for k in keywords):
            return level
    return 'none'


def get_skill_score(resume_text, jd_text):
    resume_skills = extract_skills_flat(resume_text)
    jd_skills = extract_skills_flat(jd_text)
    if not jd_skills:
        return 0.0
    matched = resume_skills & jd_skills
    return round(len(matched) / len(jd_skills), 4)


def get_experience_score(resume_text, jd_text):
    candidate_exp = extract_years(resume_text)
    required_exp = extract_years(jd_text) or 2
    if candidate_exp == 0:
        return 0.1
    if candidate_exp >= required_exp:
        return 1.0
    return round(candidate_exp / required_exp, 4)


def get_education_score(resume_text, jd_text):
    candidate_val = EDU_RANK[detect_education(resume_text)]
    required_val = EDU_RANK[detect_education(jd_text)] or 2
    if candidate_val >= required_val:
        return 1.0
    if candidate_val == 0:
        return 0.1
    return round(candidate_val / required_val, 4)


def get_keyword_density_score(resume_text, jd_text):
    jd_words = set(w.lower() for w in re.findall(r'\b\w+\b', jd_text) if len(w) > 3)
    if not jd_words:
        return 0.0
    resume_lower = resume_text.lower()
    matched = sum(1 for w in jd_words if w in resume_lower)
    return round(min(matched / len(jd_words), 1.0), 4)


def analyze_gap(resume_text, jd_text):
    resume_skills = extract_skills_flat(resume_text)
    jd_skills = extract_skills_flat(jd_text)
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    bonus = resume_skills - jd_skills
    match_pct = len(matched) / len(jd_skills) * 100 if jd_skills else 0

    if match_pct >= 80:
        fit_label = 'Strong Fit'
        fit_color = '#22c55e'
    elif match_pct >= 60:
        fit_label = 'Good Fit'
        fit_color = '#84cc16'
    elif match_pct >= 40:
        fit_label = 'Partial Fit'
        fit_color = '#f59e0b'
    else:
        fit_label = 'Poor Fit'
        fit_color = '#ef4444'

    return {
        'matched_skills': sorted(list(matched)),
        'missing_skills': sorted(list(missing)),
        'bonus_skills':   sorted(list(bonus)),
        'total_required': len(jd_skills),
        'total_matched':  len(matched),
        'total_missing':  len(missing),
        'total_bonus':    len(bonus),
        'match_percent':  round(match_pct, 1),
        'fit_label':      fit_label,
        'fit_color':      fit_color,
    }


def rank_resumes(df, job_description, top_n=10, category=None):
    filtered = df.copy()
    if category and category != 'All':
        filtered = df[df['Category'] == category].reset_index(drop=True)

    if filtered.empty:
        return pd.DataFrame()

    resumes = filtered['Resume'].fillna('').tolist()
    cleaned = [clean_text(r) for r in resumes]
    cleaned_jd = clean_text(job_description)

    # TF-IDF scores
    try:
        corpus = cleaned + [cleaned_jd]
        tfidf = TfidfVectorizer(max_features=1500, ngram_range=(1, 2), stop_words='english')
        vectors = tfidf.fit_transform(corpus)
        jd_vec = vectors[-1]
        resume_vecs = vectors[:-1]
        tfidf_scores = cosine_similarity(jd_vec, resume_vecs)[0]
    except:
        tfidf_scores = np.zeros(len(filtered))

    results = []
    for i, (_, row) in enumerate(filtered.iterrows()):
        resume_text = row['Resume'] if isinstance(row['Resume'], str) else ''

        s1 = get_skill_score(resume_text, job_description)
        s2 = float(tfidf_scores[i])
        s3 = get_experience_score(resume_text, job_description)
        s4 = get_education_score(resume_text, job_description)
        s5 = get_keyword_density_score(resume_text, job_description)

        final = (s1 * WEIGHTS['skill_match'] + s2 * WEIGHTS['tfidf_similarity'] +
                 s3 * WEIGHTS['experience'] + s4 * WEIGHTS['education'] +
                 s5 * WEIGHTS['keyword_density'])

        gap = analyze_gap(resume_text, job_description)

        results.append({
            'category':        row['Category'],
            'skill_score':     round(s1 * 100, 1),
            'tfidf_score':     round(s2 * 100, 1),
            'exp_score':       round(s3 * 100, 1),
            'edu_score':       round(s4 * 100, 1),
            'keyword_score':   round(s5 * 100, 1),
            'final_score':     round(final * 100, 1),
            'matched_skills':  gap['matched_skills'],
            'missing_skills':  gap['missing_skills'],
            'bonus_skills':    gap['bonus_skills'],
            'match_percent':   gap['match_percent'],
            'fit_label':       gap['fit_label'],
            'fit_color':       gap['fit_color'],
            'experience_years': extract_years(resume_text),
            'education':       detect_education(resume_text),
            'resume_preview':  resume_text[:300] + '...' if len(resume_text) > 300 else resume_text,
        })

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values('final_score', ascending=False).reset_index(drop=True)
    results_df.insert(0, 'rank', results_df.index + 1)
    return results_df.head(top_n)
