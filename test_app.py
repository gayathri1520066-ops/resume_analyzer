from app import app
from resume_parser import extract_resume_details


def test_home_page_renders():
    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200
    assert b"Upload" in response.data


def test_extract_resume_details_extracts_fields_and_role():
    text = '''
    G.Gayathri
    gayathri1520066@gmail.com
    7731918115
    B.Tech in CSE(AI-ML)
    Expected Graduation: 2028
    Skills: Python, Machine Learning, Data Analysis, HTML, NumPy, Pandas, Scikit-learn
    '''

    details = extract_resume_details(text)

    assert details["name"] == "G.Gayathri"
    assert details["email"] == "gayathri1520066@gmail.com"
    assert details["phone"] == "7731918115"
    assert "2028" in details["graduation_year"]
    assert "Python" in details["skills"]
    assert "AI/ML" in details["job_role"] or "Machine Learning" in details["job_role"]


def test_extract_resume_details_handles_non_it_roles():
    text = '''
    R. Priya
    priya@example.com
    9876543210
    B.Com
    Skills: Communication, Sales, Customer Service, Marketing, Negotiation, Excel
    '''

    details = extract_resume_details(text)

    assert details["name"] == "R. Priya"
    assert details["email"] == "priya@example.com"
    assert "Sales" in details["job_role"] or "Business" in details["job_role"] or "General" in details["job_role"]
    assert "improve" in details["skill_gap_summary"].lower()
