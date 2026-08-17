"""
Role definitions and matching configuration.
Easy to extend and maintain.
"""

ROLE_DEFINITIONS = {
    "HR/Admin": {
        "keywords": [
            "communication", "recruitment", "documentation", "coordination",
            "ms office", "organization", "employee relations", "hr", "admin",
            "interviews", "talent acquisition", "onboarding", "payroll"
        ],
        "weights": {
            "communication": 20,
            "recruitment": 18,
            "documentation": 15,
            "coordination": 15,
            "ms office": 10,
            "organization": 12,
            "employee relations": 10,
        },
        "badge_color": "#3b82f6",  # Blue
    },
    "Customer Support": {
        "keywords": [
            "communication", "customer service", "problem solving", "crm",
            "support", "teamwork", "customer handling", "helpdesk", "tickets",
            "troubleshooting", "escalation", "patience", "empathy"
        ],
        "weights": {
            "communication": 18,
            "customer service": 20,
            "problem solving": 17,
            "crm": 12,
            "support": 15,
            "teamwork": 10,
            "customer handling": 15,
        },
        "badge_color": "#10b981",  # Green
    },
    "Sales": {
        "keywords": [
            "sales", "communication", "negotiation", "customer handling",
            "presentation", "business development", "lead generation",
            "closing deals", "client relationship", "revenue", "crm"
        ],
        "weights": {
            "sales": 22,
            "communication": 18,
            "negotiation": 16,
            "customer handling": 14,
            "presentation": 12,
            "business development": 10,
            "lead generation": 12,
        },
        "badge_color": "#f59e0b",  # Orange
    },
    "Marketing": {
        "keywords": [
            "marketing", "digital marketing", "social media", "seo",
            "content", "analytics", "branding", "campaign", "copywriting",
            "design", "advertising", "market research"
        ],
        "weights": {
            "marketing": 20,
            "digital marketing": 16,
            "social media": 14,
            "seo": 12,
            "content": 12,
            "analytics": 14,
            "branding": 10,
        },
        "badge_color": "#ec4899",  # Pink
    },
    "Finance": {
        "keywords": [
            "accounting", "finance", "excel", "tally", "taxation", "bookkeeping",
            "ledger", "gst", "audit", "financial analysis", "reporting",
            "compliance", "invoicing"
        ],
        "weights": {
            "accounting": 20,
            "finance": 18,
            "excel": 16,
            "tally": 12,
            "taxation": 14,
            "bookkeeping": 10,
            "reporting": 10,
        },
        "badge_color": "#8b5cf6",  # Purple
    },
    "Operations": {
        "keywords": [
            "operations", "coordination", "planning", "documentation",
            "process management", "supply chain", "inventory", "quality",
            "scheduling", "logistics", "efficiency", "process improvement"
        ],
        "weights": {
            "operations": 18,
            "coordination": 16,
            "planning": 14,
            "documentation": 12,
            "process management": 16,
            "scheduling": 10,
            "quality": 10,
        },
        "badge_color": "#14b8a6",  # Teal
    },
    "IT/Software": {
        "keywords": [
            "python", "java", "sql", "javascript", "html", "css",
            "machine learning", "web development", "cloud", "programming",
            "database", "api", "debugging", "git", "linux"
        ],
        "weights": {
            "python": 18,
            "java": 16,
            "sql": 14,
            "javascript": 14,
            "web development": 12,
            "machine learning": 12,
            "cloud": 10,
            "programming": 12,
        },
        "badge_color": "#06b6d4",  # Cyan
    },
    "Data Analysis": {
        "keywords": [
            "data analysis", "excel", "pandas", "numpy", "sql", "power bi",
            "tableau", "statistics", "python", "visualization", "reporting",
            "metrics", "insights"
        ],
        "weights": {
            "data analysis": 18,
            "excel": 16,
            "pandas": 12,
            "numpy": 10,
            "sql": 14,
            "power bi": 12,
            "tableau": 12,
            "statistics": 12,
        },
        "badge_color": "#6366f1",  # Indigo
    },
}


def get_all_roles():
    """Return list of all available roles."""
    return list(ROLE_DEFINITIONS.keys())


def get_role_definition(role_name):
    """Get configuration for a specific role."""
    return ROLE_DEFINITIONS.get(role_name)


def get_role_keywords(role_name):
    """Get keywords for a role."""
    role = ROLE_DEFINITIONS.get(role_name)
    return role["keywords"] if role else []


def get_role_weights(role_name):
    """Get skill weights for a role."""
    role = ROLE_DEFINITIONS.get(role_name)
    return role["weights"] if role else {}


def get_role_color(role_name):
    """Get badge color for a role."""
    role = ROLE_DEFINITIONS.get(role_name)
    return role.get("badge_color", "#6b7280")
