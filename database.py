import sqlite3
import json
from datetime import datetime

DB_NAME = "resume_analysis.db"


def init_db():
    """Initialize the database with enhanced candidates table."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Drop old table if exists (for schema migration)
    cursor.execute("DROP TABLE IF EXISTS candidates")
    
    cursor.execute("""
        CREATE TABLE candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            phone TEXT,
            location TEXT,
            education TEXT,
            degree TEXT,
            experience TEXT,
            certifications TEXT,
            skills TEXT,
            graduation_year TEXT,
            primary_role TEXT,
            match_score INTEGER DEFAULT 0,
            skill_strengths TEXT,
            skill_gaps TEXT,
            resume_suggestions TEXT,
            all_roles JSON,
            resume_text TEXT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create job_matches table for job description matching
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS job_matches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            candidate_id INTEGER NOT NULL,
            job_description TEXT,
            match_score INTEGER DEFAULT 0,
            matching_skills TEXT,
            missing_skills TEXT,
            recommendation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(candidate_id) REFERENCES candidates(id)
        )
    """)
    
    conn.commit()
    conn.close()


def save_candidate(candidate_data):
    """Save candidate analysis to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO candidates 
        (name, email, phone, location, education, degree, experience, certifications,
         skills, graduation_year, primary_role, match_score, skill_strengths, 
         skill_gaps, resume_suggestions, all_roles, resume_text)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        candidate_data.get("name"),
        candidate_data.get("email"),
        candidate_data.get("phone"),
        candidate_data.get("location"),
        candidate_data.get("education"),
        candidate_data.get("degree"),
        candidate_data.get("experience"),
        candidate_data.get("certifications"),
        candidate_data.get("skills"),
        candidate_data.get("graduation_year"),
        candidate_data.get("primary_role"),
        candidate_data.get("match_score", 0),
        json.dumps(candidate_data.get("skill_strengths", [])),
        json.dumps(candidate_data.get("skill_gaps", [])),
        json.dumps(candidate_data.get("resume_suggestions", [])),
        json.dumps(candidate_data.get("all_roles", [])),
        candidate_data.get("resume_text"),
    ))
    conn.commit()
    candidate_id = cursor.lastrowid
    conn.close()
    return candidate_id


def get_all_candidates():
    """Retrieve all candidates from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, primary_role, match_score, skills, upload_date 
        FROM candidates 
        ORDER BY upload_date DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_candidate_by_id(candidate_id):
    """Retrieve a specific candidate by ID."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates WHERE id = ?", (candidate_id,))
    row = cursor.fetchone()
    conn.close()
    return row


def search_candidates(search_term):
    """Search candidates by name, email, or skills."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    search_param = f"%{search_term}%"
    cursor.execute("""
        SELECT id, name, email, primary_role, match_score, skills, upload_date 
        FROM candidates 
        WHERE name LIKE ? OR email LIKE ? OR skills LIKE ?
        ORDER BY upload_date DESC
    """, (search_param, search_param, search_param))
    rows = cursor.fetchall()
    conn.close()
    return rows


def filter_candidates_by_role(role):
    """Get all candidates matching a specific role."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, primary_role, match_score, skills, upload_date 
        FROM candidates 
        WHERE primary_role = ?
        ORDER BY match_score DESC
    """, (role,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def filter_candidates_by_score(min_score, max_score=100):
    """Get candidates within a specific match score range."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, email, primary_role, match_score, skills, upload_date 
        FROM candidates 
        WHERE match_score >= ? AND match_score <= ?
        ORDER BY match_score DESC
    """, (min_score, max_score))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_dashboard_stats():
    """Get statistics for dashboard."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Total candidates
    cursor.execute("SELECT COUNT(*) FROM candidates")
    total_candidates = cursor.fetchone()[0]
    
    # Average match score
    cursor.execute("SELECT AVG(match_score) FROM candidates")
    avg_score = cursor.fetchone()[0] or 0
    
    # Top recommended role
    cursor.execute("""
        SELECT primary_role, COUNT(*) as count 
        FROM candidates 
        WHERE primary_role IS NOT NULL
        GROUP BY primary_role 
        ORDER BY count DESC 
        LIMIT 1
    """)
    top_role_result = cursor.fetchone()
    top_role = top_role_result[0] if top_role_result else "Not Available"
    
    # Role distribution
    cursor.execute("""
        SELECT primary_role, COUNT(*) as count 
        FROM candidates 
        WHERE primary_role IS NOT NULL
        GROUP BY primary_role 
        ORDER BY count DESC
    """)
    role_distribution = cursor.fetchall()
    
    # Match score distribution
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN match_score >= 90 THEN 1 ELSE 0 END) as excellent,
            SUM(CASE WHEN match_score >= 75 AND match_score < 90 THEN 1 ELSE 0 END) as good,
            SUM(CASE WHEN match_score >= 60 AND match_score < 75 THEN 1 ELSE 0 END) as moderate,
            SUM(CASE WHEN match_score < 60 THEN 1 ELSE 0 END) as low
        FROM candidates
    """)
    score_dist = cursor.fetchone()
    
    # Recent candidates
    cursor.execute("""
        SELECT id, name, email, primary_role, match_score, skills, upload_date 
        FROM candidates 
        ORDER BY upload_date DESC 
        LIMIT 5
    """)
    recent = cursor.fetchall()
    
    conn.close()
    
    return {
        "total_candidates": total_candidates,
        "avg_score": round(avg_score, 1),
        "top_role": top_role,
        "role_distribution": role_distribution,
        "score_distribution": {
            "excellent": score_dist[0] or 0,
            "good": score_dist[1] or 0,
            "moderate": score_dist[2] or 0,
            "low": score_dist[3] or 0,
        },
        "recent_candidates": recent,
    }


def save_job_match(candidate_id, job_description, match_score, matching_skills, missing_skills, recommendation):
    """Save job match result."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO job_matches 
        (candidate_id, job_description, match_score, matching_skills, missing_skills, recommendation)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        candidate_id,
        job_description,
        match_score,
        json.dumps(matching_skills),
        json.dumps(missing_skills),
        recommendation,
    ))
    conn.commit()
    job_match_id = cursor.lastrowid
    conn.close()
    return job_match_id


def get_job_matches_by_candidate(candidate_id):
    """Get all job matches for a candidate."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, job_description, match_score, matching_skills, missing_skills, recommendation, created_at 
        FROM job_matches 
        WHERE candidate_id = ?
        ORDER BY created_at DESC
    """, (candidate_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows
