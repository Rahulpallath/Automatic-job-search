import requests
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage
import time

# Configuration
KEYWORDS = ["frontend developer", "software engineer", "AI engineer"]
LOCATION = "United States"
EMAIL = "youremail@gmail.com"
PASSWORD = "your_app_password"  # Use app-specific password or store securely
RECIPIENT = "youremail@gmail.com"
SENT_JOBS = set()  # Avoid duplicates

def fetch_jobs():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    for keyword in KEYWORDS:
        query = keyword.replace(" ", "%20")
        url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location={LOCATION}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        
        jobs = soup.find_all("a", class_="base-card__full-link")
        new_jobs = []
        
        for job in jobs:
            job_title = job.get_text(strip=True)
            job_link = job['href']
            if job_link not in SENT_JOBS:
                SENT_JOBS.add(job_link)
                new_jobs.append(f"{job_title}\n{job_link}")
        
        if new_jobs:
            send_email_alert(keyword, new_jobs)

def send_email_alert(keyword, jobs_list):
    msg = EmailMessage()
    msg["Subject"] = f"New LinkedIn Jobs for: {keyword}"
    msg["From"] = EMAIL
    msg["To"] = RECIPIENT
    msg.set_content("\n\n".join(jobs_list))
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL, PASSWORD)
        smtp.send_message(msg)
        print(f"Sent {len(jobs_list)} new job alerts for '{keyword}'.")

if __name__ == "__main__":
    while True:
        fetch_jobs()
        time.sleep(3600)  # Check every hour (adjust as needed)
