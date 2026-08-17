# 📄 Resume Analyzer

> **An intelligent web-based Resume Analyzer that extracts resume information, evaluates candidate profiles, and provides structured insights to help improve resume quality and job relevance.**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20Framework-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-003B57?logo=sqlite)
![HTML5](https://img.shields.io/badge/Frontend-HTML5-orange?logo=html5)
![CSS3](https://img.shields.io/badge/Styling-CSS3-blue?logo=css3)
![GitHub](https://img.shields.io/badge/Version%20Control-GitHub-black?logo=github)

---

## 📌 Overview

**Resume Analyzer** is a Python-based web application designed to analyze resumes and convert unstructured resume content into meaningful, structured information.

The application allows users to upload a resume, extract important details from the document, analyze the candidate's profile, and generate useful insights based on the resume content.

The project demonstrates the practical use of **Python, Flask, PDF text extraction, data processing, scoring logic, database management, and web development** in a single application.

---

## 🎯 Objectives

The main objectives of this project are:

* 📄 Extract useful information from uploaded resumes.
* 👤 Identify candidate details such as name and contact information.
* 🎓 Extract education and qualification details.
* 💼 Identify professional experience and skills.
* 🧠 Analyze the resume using predefined scoring criteria.
* 📊 Generate a resume score and meaningful insights.
* 🗄️ Store relevant resume information using a database.
* 🌐 Provide a simple and user-friendly web interface.
* 🚀 Demonstrate how AI/data-processing concepts can be integrated into a real-world application.

---

## ✨ Key Features

### 📤 Resume Upload

Users can upload their resumes through the web interface.

Supported resume format:

* PDF

### 📑 Resume Text Extraction

The application extracts readable text from uploaded PDF resumes and processes the extracted content for further analysis.

### 👤 Candidate Information Extraction

The system can identify relevant candidate information, including:

* Name
* Email
* Phone number
* Education
* Skills
* Experience
* Other resume-related information

### 🧠 Resume Analysis

The extracted resume information is processed using predefined analysis and scoring logic.

The analyzer evaluates important aspects of the resume and generates a structured result.

### 📊 Resume Scoring

The system provides a score based on the information and criteria identified from the resume.

This helps users understand the overall quality and completeness of their resume.

### 💡 Resume Insights

The application can provide useful observations based on the extracted resume information, helping users identify areas that may need improvement.

### 🗄️ Database Integration

Resume-related information can be stored and managed using **SQLite**, providing lightweight local database functionality.

### 🌐 Web Interface

The application provides a browser-based interface built using:

* HTML
* CSS
* Flask
* Jinja templates

---

# 🏗️ Project Architecture

```text
                    ┌──────────────────────┐
                    │        User          │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │   Flask Web App      │
                    │       app.py         │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Resume Upload       │
                    │       PDF            │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Resume Parser        │
                    │ resume_parser.py     │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Information          │
                    │ Extraction           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Scoring / Analysis   │
                    │      Service         │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    ▼                      ▼
          ┌──────────────────┐   ┌──────────────────┐
          │ SQLite Database  │   │ Web Results      │
          └──────────────────┘   └──────────────────┘
```

---

# 📂 Project Structure

```text
resume_analyzer/
│
├── app.py
├── database.py
├── resume_parser.py
├── requirements.txt
├── README.md
│
├── templates/
│   ├── ...
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── ...
│
├── uploads/
│   └── ...
│
└── .gitignore
```

### Main Components

| File / Folder      | Purpose                                          |
| ------------------ | ------------------------------------------------ |
| `app.py`           | Main Flask application and route handling        |
| `resume_parser.py` | Resume PDF processing and information extraction |
| `database.py`      | Database initialization and database operations  |
| `templates/`       | HTML/Jinja web pages                             |
| `static/`          | CSS, JavaScript and static assets                |
| `uploads/`         | Temporary/storage location for uploaded resumes  |
| `requirements.txt` | Python dependencies                              |
| `README.md`        | Project documentation                            |

---

# ⚙️ Technologies Used

## Backend

* **Python**
* **Flask**

## Resume Processing

* PDF text extraction
* Python-based text processing
* Resume information extraction

## Database

* **SQLite**

## Frontend

* HTML5
* CSS3
* JavaScript
* Jinja2 Templates

## Development Tools

* Visual Studio Code
* Git
* GitHub
* Python Virtual Environment

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/gayathri1520066-ops/resume_analyzer.git
```

Move into the project directory:

```bash
cd resume_analyzer
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
python app.py
```

The application should start on the local Flask server.

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

---

# 🖥️ How to Use

### Step 1 — Open the Application

Launch the Flask application and open it in your browser.

### Step 2 — Upload Resume

Select a resume in PDF format and upload it.

### Step 3 — Resume Processing

The application extracts the text from the uploaded resume.

### Step 4 — Information Extraction

Important resume information is identified and processed.

### Step 5 — Resume Analysis

The extracted information is evaluated using the application's scoring and analysis logic.

### Step 6 — View Results

The user receives structured information and resume analysis results through the web interface.

---

# 📊 Example Workflow

```text
Upload Resume
      ↓
PDF Text Extraction
      ↓
Text Cleaning & Processing
      ↓
Information Extraction
      ↓
Skill / Education / Experience Analysis
      ↓
Resume Scoring
      ↓
Generate Results
      ↓
Display Results
```

---

# 🔐 Data & Privacy

Resume files may contain sensitive personal information.

When deploying this application in a production environment:

* Protect uploaded files.
* Avoid exposing uploaded resumes publicly.
* Validate uploaded file types.
* Limit maximum upload size.
* Sanitize filenames.
* Secure stored candidate information.
* Use appropriate authentication and authorization.
* Remove temporary files when they are no longer required.

For development purposes, uploaded files should be handled carefully and should not be committed to GitHub.

---

# 🧪 Testing

Before deployment, test the application with resumes containing different:

* Education formats
* Skill sets
* Experience levels
* Resume layouts
* Contact information formats
* PDF structures

Also verify:

* Invalid file uploads
* Empty resumes
* Corrupted PDFs
* Missing fields
* Database operations
* Scoring behavior

---

# 🔮 Future Enhancements

The project can be extended with more advanced features such as:

### 🤖 AI-Based Resume Analysis

Integrate NLP or Large Language Models to provide deeper resume analysis.

### 🎯 Job Description Matching

Allow users to enter a job description and calculate how closely their resume matches the required skills.

### 📈 ATS Compatibility Score

Add an Applicant Tracking System (ATS) compatibility analysis.

### 🔍 Skill Gap Analysis

Identify missing skills by comparing the candidate's resume with a target job description.

### 📊 Advanced Dashboard

Create visual dashboards showing:

* Resume score
* Skill distribution
* Experience summary
* Education analysis
* Job-match percentage

### 📄 Resume Improvement Suggestions

Generate personalized suggestions for improving:

* Professional summary
* Skills section
* Experience descriptions
* Keywords
* Formatting

### 🔐 User Authentication

Add secure user registration and login functionality.

### ☁️ Cloud Deployment

Deploy the application using platforms such as:

* Render
* Railway
* AWS
* Azure

---

# 📈 Future System Vision

The long-term goal is to transform the project from a basic resume analyzer into a complete **AI-powered career assistance platform**.

```text
                    Resume
                       │
                       ▼
              Resume Analyzer
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Skills      Experience    Education
          │            │            │
          └────────────┼────────────┘
                       ▼
                 Resume Score
                       │
                       ▼
              Job Description
                       │
                       ▼
               Match Analysis
                       │
              ┌────────┴────────┐
              ▼                 ▼
        Skill Gap Analysis   Suggestions
              │                 │
              └────────┬────────┘
                       ▼
              Career Insights
```

---

# 🤝 Contributing

Contributions are welcome.

If you would like to improve this project:

1. Fork the repository.
2. Create a new branch.

```bash
git checkout -b feature/your-feature
```

3. Make your changes.
4. Commit your changes.

```bash
git add .
git commit -m "Add new feature"
```

5. Push the branch.

```bash
git push origin feature/your-feature
```

6. Open a Pull Request.

---

# 📝 Learning Outcomes

This project provides practical experience in:

* Python application development
* Flask web development
* PDF processing
* Text extraction
* Data processing
* Database integration
* Web application architecture
* Git and GitHub
* Virtual environments
* Frontend/backend integration
* Building real-world software projects

---

# 👩‍💻 Author

**Gayathri G**

B.Tech — Computer Science / CSM

Interested in:

* Python
* Machine Learning
* Artificial Intelligence
* Data Science
* Web Development

---

# ⭐ Support

If you find this project useful or interesting, consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is intended for educational and development purposes.

If you plan to distribute or deploy the project publicly, consider adding an appropriate open-source license such as the MIT License.

---

## 🔗 Repository

**GitHub:**
https://github.com/gayathri1520066-ops/resume_analyzer

---

> **Resume Analyzer — Turning resumes into structured insights.**
