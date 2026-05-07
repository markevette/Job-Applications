# send_email.py
import os
import json
import argparse
import smtplib
from email.message import EmailMessage

def main(jobs_path: str):
    email_to = os.environ["EMAIL_TO"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    email_from = email_to  # or a dedicated sender

    with open(jobs_path, encoding="utf-8") as f:
        jobs = json.load(f)

    body_lines = []
    for j in jobs:
        body_lines.append(
            f"- {j.get('title')} @ {j.get('company','?')}\n"
            f"  Link: {j.get('url','')}\n"
            f"  Doc: {j.get('google_doc_link','')}\n"
        )
    body = "Here are today's tailored resumes:\n\n" + "\n".join(body_lines)

    msg = EmailMessage()
    msg["Subject"] = "Daily tailored resumes"
    msg["From"] = email_from
    msg["To"] = email_to
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_from, app_password)
        smtp.send_message(msg)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", required=True)
    args = parser.parse_args()
    main(args.jobs)
