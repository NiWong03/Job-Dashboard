import requests
import re
from datetime import datetime, timedelta, timezone

def scrape_github_simplifyjobs():
    url = "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/refs/heads/dev/README.md"
    response = requests.get(url)
    lines = response.text.splitlines()

    jobs = []
    parsing = False
    current_section = None

    for line in lines:
        # Find the markdown table section
        if line.startswith("| Company | Role | Location | Application | Age |"):
            parsing = True
            continue
            
        if parsing:
            if line.strip() == "" or line.startswith("## "):
                parsing = False
                continue
            if line.startswith("|-") or line.startswith("| -"):  # Skip header separator line
                continue
            if not line.startswith("|"):  # Skip non-table lines
                continue
                
            columns = [col.strip() for col in line.split("|")[1:-1]]
            if len(columns) >= 5:
                company, role, location, apply_link, age = columns
                
                # Skip entries that are just arrows or formatting
                if company.strip() in ['↳', ''] or role.strip() in ['↳', '']:
                    continue
                
                # Extract company name (remove markdown formatting)
                company_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', company)
                company_clean = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', company_clean)
                company_clean = company_clean.strip()
                
                # Extract role name (remove markdown formatting)
                role_clean = re.sub(r'\*\*(.*?)\*\*', r'\1', role)
                role_clean = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', role_clean)
                role_clean = role_clean.strip()
                
                # Clean location (remove HTML tags)
                location_clean = re.sub(r'<br>', ', ', location)
                location_clean = re.sub(r'<.*?>', '', location_clean)
                location_clean = location_clean.strip()
                
                # Parse age to get date posted
                date_posted = parse_age_to_date(age)
                
                # Extract URL from apply link
                url = extract_url_from_md(apply_link)
                
                # Only add jobs with valid data
                if company_clean and role_clean and url:
                    jobs.append({
                        "source": "github_simplifyjobs",
                        "title": role_clean,
                        "company": company_clean,
                        "location": location_clean,
                        "date_posted": date_posted,
                        "url": url,
                    })
    return jobs

def parse_age_to_date(age_str):
    """Convert age string like '0d', '1d', '2d' to a date"""
    try:
        age_str = age_str.strip()
        if age_str.endswith('d'):
            days = int(age_str[:-1])
            return (datetime.now(timezone.utc) - timedelta(days=days)).date()
        else:
            return datetime.now(timezone.utc).date()
    except:
        return datetime.now(timezone.utc).date()

def parse_md_date(date_str):
    try:
        return datetime.strptime(date_str.strip(), "%m/%d/%y").date()
    except:
        return datetime.now(timezone.utc).date()

def extract_url_from_md(md):
    # Remove image tags
    md = re.sub(r'<img.*?>', '', md)
    # Try to find HTML anchor tag
    match = re.search(r'<a [^>]*href="([^"]+)"', md)
    if match:
        return match.group(1)
    # Try to find markdown link format [text](url)
    match = re.search(r"\[.*?\]\((https?://[^\)]+)\)", md)
    if match:
        return match.group(1)
    # Try to find direct link
    match = re.search(r"(https?://[^\s\)]+)", md)
    if match:
        return match.group(1)
    return None
