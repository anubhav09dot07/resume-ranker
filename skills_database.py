SKILLS_DB = {
    "Programming Languages": [
        "python", "java", "javascript", "c++", "c#", "r", "scala",
        "golang", "ruby", "php", "swift", "kotlin", "typescript", "matlab"
    ],
    "ML & Data Science": [
        "machine learning", "deep learning", "neural network",
        "scikit-learn", "tensorflow", "keras", "pytorch", "xgboost",
        "random forest", "nlp", "computer vision", "data science",
        "reinforcement learning", "transfer learning", "pandas", "numpy"
    ],
    "Data & Databases": [
        "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
        "cassandra", "oracle", "sqlite", "nosql", "hadoop", "spark", "hive"
    ],
    "Cloud & DevOps": [
        "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
        "ci/cd", "terraform", "ansible", "linux", "git", "github", "gitlab"
    ],
    "Web & Frameworks": [
        "django", "flask", "fastapi", "react", "angular", "vue",
        "node.js", "spring boot", "rest api", "graphql", "html", "css", "bootstrap"
    ],
    "Data Analysis": [
        "matplotlib", "seaborn", "tableau", "power bi", "excel",
        "statistics", "data visualization", "jupyter", "scipy"
    ],
    "Soft Skills": [
        "leadership", "communication", "teamwork", "problem solving",
        "project management", "agile", "scrum", "jira"
    ]
}

ALL_SKILLS = [skill for category in SKILLS_DB.values() for skill in category]
