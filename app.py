
from flask import Flask, render_template, request
from PyPDF2 import PdfReader
import os
import sqlite3

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create uploads folder automatically
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    file = request.files["resume"]
    job_skills = request.form["job_skills"]

    filepath = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(filepath)

    pdf = PdfReader(filepath)

    text = ""

    for page in pdf.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    # Skills Database

    skills_database = [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "SQL",
        "TensorFlow",
        "PyTorch",
        "Flask",
        "Django",
        "Pandas",
        "NumPy",
        "Data Science",
        "Artificial Intelligence",
        "Power BI",
        "Excel",
        "Java",
        "C++"
    ]

    # Detect skills in resume

    found_skills = []

    for skill in skills_database:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    # Job skills entered by user

    job_skill_list = [
        skill.strip()
        for skill in job_skills.split(",")
    ]

    matched_skills = []
    missing_skills = []

    for skill in job_skill_list:

        if skill.lower() in text.lower():

            matched_skills.append(skill)

        else:

            missing_skills.append(skill)
            
            
            recommendations = []

        for skill in missing_skills:

         recommendations.append(
        f"Learn {skill}"
    )

    # Match score

    if len(job_skill_list) > 0:

        match_score = round(
            (len(matched_skills) / len(job_skill_list))
            * 100
        )

    else:

        match_score = 0
    
    # Save Analysis To Database

    conn = sqlite3.connect("resume_analyzer.db")

    cursor = conn.cursor()

    cursor.execute(
    """
    INSERT INTO analysis_history
    (filename, match_score, skills)
    VALUES (?, ?, ?)
    """,
    (
        file.filename,
        match_score,
        ", ".join(found_skills)
    )
)

    conn.commit()
    conn.close()

    return render_template(
    "result.html",
    resume_text=text,
    skills=found_skills,
    match_score=match_score,
    matched_skills=matched_skills,
    missing_skills=missing_skills,
    recommendations=recommendations
)

@app.route("/history")
def history():

    conn = sqlite3.connect("resume_analyzer.db")

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM analysis_history
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        data=data
    )


if __name__ == "__main__":
    app.run(debug=True)

