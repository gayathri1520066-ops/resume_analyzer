from flask import Flask, render_template, request, jsonify
import os
import json
from werkzeug.utils import secure_filename
from datetime import datetime

from resume_parser import extract_text_from_pdf, extract_resume_details
from database import (
    init_db, save_candidate, get_all_candidates, get_candidate_by_id,
    search_candidates, filter_candidates_by_role, filter_candidates_by_score,
    get_dashboard_stats, save_job_match
)
from scoring_service import get_score_category
from job_matching_service import (
    calculate_job_match_score, generate_job_match_recommendation
)
from role_config import get_all_roles


app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_FILE_SIZE

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static", exist_ok=True)

# Initialize database
init_db()


def allowed_file(filename):
    """Check if file is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
def dashboard():
    """Analytics dashboard."""
    stats = get_dashboard_stats()
    return render_template("dashboard.html", stats=stats)


@app.route("/analyze", methods=["POST"])
def analyze():
    """Analyze uploaded resume."""
    resume = request.files.get("resume")

    if not resume or resume.filename == "":
        return render_template("index.html", error="Please upload a resume PDF.")

    if not allowed_file(resume.filename):
        return render_template("index.html", error="Please upload a valid PDF file.")

    if resume.content_length > MAX_FILE_SIZE:
        return render_template("index.html", error="File size too large. Maximum 5MB allowed.")

    # Secure filename
    filename = secure_filename(resume.filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
    filename = timestamp + filename

    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        resume.save(file_path)
        resume_text = extract_text_from_pdf(file_path)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return render_template("index.html", error="Failed to process PDF. Please ensure it's a valid PDF file.")

    if not resume_text.strip():
        os.remove(file_path)
        return render_template("index.html", error="No readable text found in PDF. Please check the document.")

    try:
        details = extract_resume_details(resume_text)
        details["resume_text"] = resume_text[:5000]  # Store first 5000 chars
        
        # Save to database
        candidate_id = save_candidate(details)

        return render_template(
            "index.html",
            analysis_complete=True,
            candidate_id=candidate_id,
            candidate_name=details.get("name", "Candidate"),
            email=details.get("email"),
            phone=details.get("phone"),
            location=details.get("location"),
            education=details.get("education"),
            degree=details.get("degree"),
            skills=details.get("skills"),
            graduation_year=details.get("graduation_year"),
            primary_role=details.get("primary_role"),
            match_score=details.get("match_score", 0),
            all_roles=details.get("all_roles", []),
            skill_strengths=details.get("skill_strengths", []),
            skill_gaps=details.get("skill_gaps", []),
            resume_suggestions=details.get("resume_suggestions", []),
        )
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return render_template("index.html", error=f"Error analyzing resume: {str(e)}")


@app.route("/candidates")
def candidates():
    """View all candidates with search and filtering."""
    # Get query parameters
    search_term = request.args.get("search", "").strip()
    role_filter = request.args.get("role", "").strip()
    score_filter = request.args.get("score", "").strip()
    sort_by = request.args.get("sort", "newest").strip()

    all_candidates = []

    # Apply search
    if search_term:
        all_candidates = search_candidates(search_term)
    elif role_filter:
        all_candidates = filter_candidates_by_role(role_filter)
    elif score_filter:
        if score_filter == "90+":
            all_candidates = filter_candidates_by_score(90, 100)
        elif score_filter == "75-89":
            all_candidates = filter_candidates_by_score(75, 89)
        elif score_filter == "60-74":
            all_candidates = filter_candidates_by_score(60, 74)
        elif score_filter == "below60":
            all_candidates = filter_candidates_by_score(0, 59)
    else:
        all_candidates = get_all_candidates()

    # Apply sorting
    if sort_by == "highest":
        all_candidates.sort(key=lambda x: x[4], reverse=True)
    elif sort_by == "lowest":
        all_candidates.sort(key=lambda x: x[4])
    elif sort_by == "oldest":
        all_candidates.sort(key=lambda x: x[6])
    elif sort_by == "name":
        all_candidates.sort(key=lambda x: x[1] or "")

    all_roles = get_all_roles()
    
    return render_template(
        "candidates.html",
        candidates=all_candidates,
        all_roles=all_roles,
        search_term=search_term,
        role_filter=role_filter,
        score_filter=score_filter,
        sort_by=sort_by,
    )


@app.route("/candidate/<int:candidate_id>")
def candidate_detail(candidate_id):
    """View detailed candidate profile."""
    candidate = get_candidate_by_id(candidate_id)
    if not candidate:
        return render_template("error.html", error="Candidate not found."), 404

    # Parse JSON fields
    skill_strengths = json.loads(candidate[13]) if candidate[13] else []
    skill_gaps = json.loads(candidate[14]) if candidate[14] else []
    resume_suggestions = json.loads(candidate[15]) if candidate[15] else []
    all_roles = json.loads(candidate[16]) if candidate[16] else []
    
    # Get score category
    score = candidate[12] or 0
    score_category, score_color = get_score_category(score)

    return render_template(
        "candidate_detail.html",
        candidate=candidate,
        skill_strengths=skill_strengths,
        skill_gaps=skill_gaps,
        resume_suggestions=resume_suggestions,
        all_roles=all_roles,
        score_category=score_category,
        score_color=score_color,
    )


@app.route("/job-match")
def job_match():
    """Job description matching page."""
    return render_template("job_match.html")


@app.route("/api/job-match", methods=["POST"])
def api_job_match():
    """API endpoint for job matching."""
    data = request.get_json()
    candidate_id = data.get("candidate_id")
    job_description = data.get("job_description", "")

    if not candidate_id or not job_description:
        return jsonify({"error": "Missing candidate_id or job_description"}), 400

    candidate = get_candidate_by_id(candidate_id)
    if not candidate:
        return jsonify({"error": "Candidate not found"}), 404

    candidate_skills = candidate[8]  # skills field

    # Calculate match
    match_score, matching_skills, missing_skills = calculate_job_match_score(
        candidate_skills, job_description
    )

    # Generate recommendation
    recommendation = generate_job_match_recommendation(
        match_score, matching_skills, missing_skills, job_description
    )

    # Save to database
    save_job_match(candidate_id, job_description, match_score, matching_skills, missing_skills, recommendation)

    return jsonify({
        "match_score": match_score,
        "matching_skills": matching_skills,
        "missing_skills": missing_skills,
        "recommendation": recommendation,
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return render_template("error.html", error="Page not found."), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return render_template("error.html", error="Server error. Please try again."), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)