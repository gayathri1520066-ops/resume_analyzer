"""
Scoring and role matching logic.
Calculates match scores for candidates against different roles.
"""

from role_config import ROLE_DEFINITIONS, get_all_roles, get_role_weights


def calculate_role_match_score(candidate_skills, role_name):
    """
    Calculate match score for a candidate against a specific role.
    Returns a score between 0-100.
    """
    role = ROLE_DEFINITIONS.get(role_name)
    if not role:
        return 0
    
    weights = role["weights"]
    candidate_skills_lower = candidate_skills.lower()
    
    score = 0
    total_weight = sum(weights.values())
    
    for skill, weight in weights.items():
        if skill in candidate_skills_lower:
            score += weight
    
    # Normalize to 0-100
    if total_weight > 0:
        score = min(100, int((score / total_weight) * 100))
    
    return score


def calculate_all_role_scores(candidate_skills):
    """
    Calculate match scores for all roles.
    Returns dict of {role: score} sorted by score descending.
    """
    scores = {}
    for role in get_all_roles():
        score = calculate_role_match_score(candidate_skills, role)
        scores[role] = score
    
    # Sort by score descending
    return dict(sorted(scores.items(), key=lambda x: x[1], reverse=True))


def get_top_matching_roles(candidate_skills, count=5):
    """
    Get top N matching roles for a candidate.
    """
    scores = calculate_all_role_scores(candidate_skills)
    top_roles = []
    
    for role, score in list(scores.items())[:count]:
        if score > 0:  # Only include roles with some match
            top_roles.append({
                "role": role,
                "score": score,
                "matching_skills": get_matching_skills_for_role(candidate_skills, role),
            })
    
    return top_roles


def get_matching_skills_for_role(candidate_skills, role_name):
    """
    Get skills the candidate has that match the role.
    """
    role = ROLE_DEFINITIONS.get(role_name)
    if not role:
        return []
    
    candidate_skills_lower = candidate_skills.lower()
    matching = []
    
    for skill in role["keywords"]:
        if skill in candidate_skills_lower:
            matching.append(skill.title())
    
    return matching


def get_skill_gaps_for_role(candidate_skills, role_name):
    """
    Get skills missing for a specific role.
    """
    role = ROLE_DEFINITIONS.get(role_name)
    if not role:
        return []
    
    candidate_skills_lower = candidate_skills.lower()
    gaps = []
    
    for skill in role["keywords"]:
        if skill not in candidate_skills_lower:
            gaps.append(skill.title())
    
    return gaps[:5]  # Return top 5 gaps


def calculate_education_fit(education_text, role_name):
    """
    Calculate how well education matches the role.
    Returns score 0-100.
    """
    education_lower = education_text.lower()
    score = 0
    
    # Role-specific education keywords
    education_keywords = {
        "IT/Software": ["b.tech", "bachelor", "computer science", "it", "engineering", "degree"],
        "Finance": ["b.com", "commerce", "accounting", "mba", "ca", "degree"],
        "Marketing": ["marketing", "mba", "commerce", "advertising", "degree"],
        "Sales": ["mba", "business", "commerce", "sales", "degree"],
        "HR/Admin": ["hr", "human resources", "business", "management", "degree"],
        "Operations": ["operations", "supply chain", "business", "management", "degree"],
        "Customer Support": ["any", "high school"],  # Any education ok
        "Data Analysis": ["b.tech", "statistics", "math", "computer science", "degree"],
    }
    
    relevant_keywords = education_keywords.get(role_name, [])
    
    for keyword in relevant_keywords:
        if keyword in education_lower:
            score += 20
    
    return min(100, score)


def calculate_experience_fit(experience_text, role_name):
    """
    Calculate how well experience matches the role.
    Returns score 0-100.
    """
    experience_lower = experience_text.lower()
    score = 0
    
    # Role-specific experience keywords
    experience_keywords = {
        "IT/Software": ["developer", "programmer", "engineer", "coding", "project", "team"],
        "Finance": ["accountant", "financial", "audit", "tax", "analyst"],
        "Marketing": ["campaign", "promotion", "branding", "marketing", "advertising"],
        "Sales": ["sales", "client", "negotiation", "closing", "revenue"],
        "HR/Admin": ["recruitment", "hr", "employee", "coordination", "admin"],
        "Operations": ["operations", "process", "coordination", "supply chain"],
        "Customer Support": ["customer", "support", "service", "help", "client"],
        "Data Analysis": ["analysis", "analytics", "data", "insights", "reporting"],
    }
    
    relevant_keywords = experience_keywords.get(role_name, [])
    
    for keyword in relevant_keywords:
        if keyword in experience_lower:
            score += 12
    
    return min(100, score)


def get_resume_quality_score(candidate_data):
    """
    Evaluate resume completeness and quality.
    Returns score 0-100.
    """
    score = 0
    max_points = 0
    
    # Check each field
    checks = [
        ("name", 15),
        ("email", 15),
        ("phone", 15),
        ("education", 20),
        ("skills", 20),
        ("experience", 15),
    ]
    
    for field, points in checks:
        max_points += points
        value = candidate_data.get(field, "")
        if value and str(value).strip():
            score += points
    
    if max_points > 0:
        return int((score / max_points) * 100)
    
    return 0


def calculate_comprehensive_match_score(candidate_data, role_name):
    """
    Calculate overall match score combining multiple factors.
    """
    skills_score = calculate_role_match_score(candidate_data.get("skills", ""), role_name)
    education_score = calculate_education_fit(candidate_data.get("education", ""), role_name)
    experience_score = calculate_experience_fit(candidate_data.get("experience", ""), role_name)
    quality_score = get_resume_quality_score(candidate_data)
    
    # Weighted average
    total_score = (
        (skills_score * 0.50) +
        (education_score * 0.20) +
        (experience_score * 0.20) +
        (quality_score * 0.10)
    )
    
    return min(100, int(total_score))


def get_score_category(score):
    """
    Categorize a score as Excellent, Good, Moderate, or Low.
    """
    if score >= 90:
        return "Excellent", "#10b981"  # Green
    elif score >= 75:
        return "Good", "#3b82f6"  # Blue
    elif score >= 60:
        return "Moderate", "#f59e0b"  # Orange
    else:
        return "Low", "#ef4444"  # Red
