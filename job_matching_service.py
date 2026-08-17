"""
Job description matching and analysis.
Compare candidate against job requirements.
"""

import re
from scoring_service import get_role_weights


def extract_job_requirements(job_description):
    """
    Extract skills and keywords from job description.
    """
    if not job_description:
        return []
    
    job_lower = job_description.lower()
    
    # Common skill keywords to look for
    common_skills = [
        "python", "java", "javascript", "sql", "html", "css",
        "communication", "teamwork", "leadership", "management",
        "excel", "power bi", "tableau", "salesforce", "crm",
        "data analysis", "machine learning", "ai", "cloud",
        "sales", "marketing", "customer service", "negotiation",
        "project management", "agile", "scrum", "kanban",
        "problem solving", "analytical", "strategic thinking",
        "attention to detail", "organization", "planning",
        "recruitment", "interviews", "hr", "payroll",
        "accounting", "finance", "taxation", "auditing",
        "documentation", "writing", "reporting",
        "aws", "azure", "gcp", "docker", "kubernetes",
        "react", "angular", "vue", "django", "flask",
        "mongodb", "postgresql", "mysql", "oracle",
        "rest api", "graphql", "json", "xml",
        "git", "github", "gitlab", "bitbucket",
        "ci/cd", "jenkins", "docker", "devops",
        "linux", "windows", "macos", "unix",
        "networking", "security", "encryption", "firewall",
        "mobile development", "ios", "android", "react native",
        "ui/ux", "figma", "adobe xd", "design thinking",
    ]
    
    found_skills = []
    for skill in common_skills:
        if skill in job_lower:
            found_skills.append(skill)
    
    return found_skills


def calculate_job_match_score(candidate_skills, job_description):
    """
    Calculate how well candidate matches the job description.
    Returns score 0-100 and details.
    """
    job_skills = extract_job_requirements(job_description)
    candidate_skills_lower = candidate_skills.lower()
    
    if not job_skills:
        return 0, [], []
    
    matching_skills = []
    missing_skills = []
    
    for skill in job_skills:
        if skill in candidate_skills_lower:
            matching_skills.append(skill.title())
        else:
            missing_skills.append(skill.title())
    
    # Calculate score
    if len(job_skills) > 0:
        match_percentage = (len(matching_skills) / len(job_skills)) * 100
        score = min(100, int(match_percentage * 1.2))  # Slight boost for exact matches
    else:
        score = 0
    
    return score, matching_skills, missing_skills


def generate_job_match_recommendation(match_score, matching_skills, missing_skills, job_description):
    """
    Generate a professional recommendation based on job match.
    """
    if match_score >= 85:
        return f"Excellent fit for this role. The candidate has {len(matching_skills)} of the key required skills and demonstrates strong alignment with the position requirements."
    elif match_score >= 70:
        return f"Good fit for this role. The candidate has {len(matching_skills)} of the key required skills. Recommended for interview with focus on upskilling in {missing_skills[0] if missing_skills else 'technical requirements'}."
    elif match_score >= 50:
        return f"Moderate fit for this role. The candidate has {len(matching_skills)} key skills but is missing {len(missing_skills)} important qualifications. Consider for training or junior positions."
    else:
        return f"Limited fit for this role. The candidate has only {len(matching_skills)} of the required skills. May need significant training and development for this position."


def get_improvement_suggestions(candidate_data, target_role_name=None):
    """
    Generate specific improvement suggestions for the resume.
    """
    suggestions = []
    
    # Check contact information
    if candidate_data.get("name"):
        suggestions.append({
            "type": "success",
            "message": "✓ Name detected"
        })
    else:
        suggestions.append({
            "type": "warning",
            "message": "⚠ Add your full name at the top"
        })
    
    if candidate_data.get("email"):
        suggestions.append({
            "type": "success",
            "message": "✓ Email address detected"
        })
    else:
        suggestions.append({
            "type": "warning",
            "message": "⚠ Add a professional email address"
        })
    
    if candidate_data.get("phone"):
        suggestions.append({
            "type": "success",
            "message": "✓ Phone number detected"
        })
    else:
        suggestions.append({
            "type": "warning",
            "message": "⚠ Add your contact phone number"
        })
    
    # Check education
    if candidate_data.get("education"):
        suggestions.append({
            "type": "success",
            "message": "✓ Education section detected"
        })
    else:
        suggestions.append({
            "type": "warning",
            "message": "⚠ Add your educational background"
        })
    
    # Check skills
    skills_list = [s.strip() for s in str(candidate_data.get("skills", "")).split(",") if s.strip()]
    if len(skills_list) >= 3:
        suggestions.append({
            "type": "success",
            "message": f"✓ {len(skills_list)} skills detected"
        })
    else:
        suggestions.append({
            "type": "warning",
            "message": "⚠ Add more skills (at least 5-8 relevant skills)"
        })
    
    # Check experience
    if candidate_data.get("experience"):
        suggestions.append({
            "type": "success",
            "message": "✓ Experience section detected"
        })
    else:
        suggestions.append({
            "type": "warning",
            "message": "⚠ Add your work experience and achievements"
        })
    
    # General improvement tips
    if candidate_data.get("skills"):
        suggestions.append({
            "type": "info",
            "message": "💡 Add quantifiable achievements (numbers, percentages, results)"
        })
    
    suggestions.append({
        "type": "info",
        "message": "💡 Use action verbs (Managed, Developed, Implemented, Led, etc.)"
    })
    
    suggestions.append({
        "type": "info",
        "message": "💡 Keep formatting clean and consistent throughout"
    })
    
    return suggestions
