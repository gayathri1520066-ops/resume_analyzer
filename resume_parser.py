import re
from pypdf import PdfReader
from scoring_service import (
    calculate_all_role_scores,
    get_top_matching_roles,
    calculate_comprehensive_match_score,
    get_skill_gaps_for_role,
)
from job_matching_service import get_improvement_suggestions


def extract_text_from_pdf(file_path):
    """Extract text from PDF file."""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Failed to extract PDF text: {str(e)}")


def _normalize_skill(skill):
    """Normalize a skill string."""
    skill = skill.strip()
    skill = re.sub(r"\s+", " ", skill)
    skill = skill.strip("•- ")
    return skill


def _clean_skill_tokens(text):
    """Extract skill tokens from text."""
    tokens = []
    for part in re.split(r"[•,;]", text):
        token = _normalize_skill(part)
        if token and len(token) > 1:
            tokens.append(token)
    return tokens


def extract_resume_details(resume_text):
    """
    Extract detailed information from resume text.
    Returns comprehensive candidate data.
    """
    cleaned = resume_text.replace("\xa0", " ")
    lines = [line.strip() for line in cleaned.splitlines() if line.strip()]

    # Initialize data containers
    candidate_data = {
        "name": "",
        "email": "",
        "phone": "",
        "location": "",
        "education": "",
        "degree": "",
        "experience": "",
        "certifications": "",
        "skills": "",
        "graduation_year": "",
        "primary_role": "",
        "match_score": 0,
        "skill_strengths": [],
        "skill_gaps": [],
        "resume_suggestions": [],
        "all_roles": [],
    }

    education_lines = []
    skills_lines = []
    experience_lines = []
    certifications_lines = []
    current_section = None

    # Parse resume sections
    for line in lines:
        lower = line.lower()

        # Detect sections
        if any(keyword in lower for keyword in ["objective", "professional summary", "summary"]):
            current_section = "summary"
            continue
        elif any(keyword in lower for keyword in ["education", "educational"]):
            current_section = "education"
            continue
        elif any(keyword in lower for keyword in ["skills", "technical skills", "core skills"]):
            current_section = "skills"
            continue
        elif any(keyword in lower for keyword in ["experience", "work experience", "employment", "career"]):
            current_section = "experience"
            continue
        elif any(keyword in lower for keyword in ["certifications", "certificates", "credentials"]):
            current_section = "certifications"
            continue
        elif any(keyword in lower for keyword in ["projects", "achievements", "accomplishments"]):
            current_section = "projects"
            continue

        # Extract name (first capitalized line that looks like a name)
        if not candidate_data["name"] and current_section is None:
            if re.match(r"^[A-Z][A-Za-z.\s'-]+$", line) and len(line.split()) <= 4 and len(line) < 50:
                candidate_data["name"] = line

        # Extract email
        if not candidate_data["email"]:
            email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", line)
            if email_match:
                candidate_data["email"] = email_match.group(0)

        # Extract phone
        if not candidate_data["phone"]:
            phone_match = re.search(r"\+?\d[\d\s().-]{8,}\d", line)
            if phone_match:
                candidate_data["phone"] = re.sub(r"\D", "", phone_match.group(0))

        # Extract location (usually after phone or near contact info)
        if not candidate_data["location"] and any(city in line for city in ["Mumbai", "Delhi", "Bangalore", "Chennai", "Pune", "Hyderabad", "New York", "London", "San Francisco"]):
            candidate_data["location"] = line

        # Extract graduation year
        if not candidate_data["graduation_year"]:
            year_match = re.search(r"(202[0-9]|20[0-2][0-9])", line)
            if year_match and any(kw in lower for kw in ["graduation", "expected", "graduating", "pass"]):
                candidate_data["graduation_year"] = year_match.group(1)

        # Process by section
        if current_section == "education":
            if any(kw in lower for kw in ["b.tech", "b.com", "mba", "bachelor", "master", "intermediate", "10th", "diploma", "degree"]):
                education_lines.append(line)
                if not candidate_data["degree"]:
                    degree_match = re.search(r"(B\.?Tech|B\.?Com|MBA|Bachelor|Master|Diploma|BTech|BCom)", line, re.IGNORECASE)
                    if degree_match:
                        candidate_data["degree"] = degree_match.group(0)

        elif current_section == "skills":
            skills_lines.append(line)

        elif current_section == "experience":
            experience_lines.append(line)

        elif current_section == "certifications":
            certifications_lines.append(line)

    # Finalize extracted data
    candidate_data["education"] = " | ".join(education_lines[:3]) if education_lines else ""
    candidate_data["experience"] = " | ".join(experience_lines[:5]) if experience_lines else ""
    candidate_data["certifications"] = " | ".join(certifications_lines) if certifications_lines else ""

    # Extract and clean skills
    all_skills_text = " ".join(skills_lines + [line for line in lines if any(skill_kw in line.lower() for skill_kw in ["python", "java", "excel", "communication", "leadership"])])
    skill_tokens = _clean_skill_tokens(all_skills_text)
    
    skill_set = []
    seen = set()
    for skill in skill_tokens:
        key = skill.lower()
        if key and key not in seen and key not in {"skills", "technical", "soft", "tools", "programming", "libraries", "objective", "education", "projects"}:
            seen.add(key)
            skill_set.append(skill)

    candidate_data["skills"] = ", ".join(skill_set)
    skills_lower = " ".join(skill_set).lower()

    # Calculate role matches
    role_scores = calculate_all_role_scores(candidate_data["skills"])
    
    # Get top role
    if role_scores:
        primary_role = max(role_scores, key=role_scores.get)
        candidate_data["primary_role"] = primary_role
        
        # Calculate comprehensive match score
        match_score = calculate_comprehensive_match_score(candidate_data, primary_role)
        candidate_data["match_score"] = match_score
        
        # Get skill strengths and gaps
        candidate_data["skill_strengths"] = [s.strip() for s in skill_set if s.strip()]
        candidate_data["skill_gaps"] = get_skill_gaps_for_role(candidate_data["skills"], primary_role)

    # Get all role recommendations
    candidate_data["all_roles"] = get_top_matching_roles(candidate_data["skills"], count=5)

    # Generate improvement suggestions
    candidate_data["resume_suggestions"] = get_improvement_suggestions(candidate_data, candidate_data.get("primary_role"))

    return candidate_data
