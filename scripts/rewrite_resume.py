import os
import json
import argparse
import requests
from pathlib import Path

def call_gemini(api_key: str, base_resume: str, job: dict) -> str:
    jd = job.get("description", "")
    keywords = job.get("keywords", "")
    prompt = (
        "You are a resume tailoring assistant.\n"
        "Given this base resume and job description, rewrite the resume to best match the role.\n\n"
        f"JOB DESCRIPTION:\n{jd}\n\n"
        f"EXTRACTED KEYWORDS:\n{keywords}\n\n"
        f"BASE RESUME:\n{base_resume}\n"
    )
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    resp = requests.post(url, headers=headers, params=params, json=payload)
    resp.raise_for_status()
    out = resp.json()
    return out["candidates"][0]["content"]["parts"][0]["text"]

def main(jobs_path: str, base_resume_path: str):
    api_key = os.environ["GEMINI_API_KEY"]
    base_resume = Path(base_resume_path).read_text(encoding="utf-8")

    with open(jobs_path, encoding="utf-8") as f:
        jobs = json.load(f)

    for j in jobs:
        tailored = call_gemini(api_key, base_resume, j)
        j["tailored_resume"] = tailored

    with open(jobs_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", required=True)
    parser.add_argument("--base", required=True)
    args = parser.parse_args()
    main(args.jobs, args.base)
