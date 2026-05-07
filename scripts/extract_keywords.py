import os
import json
import argparse
import requests

def extract_for_job(job, api_key: str):
    jd = job.get("description", "")
    prompt = f"Extract key skills and responsibilities from this job description:\n\n{jd}"
    # TODO: replace with actual Gemini endpoint
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    resp = requests.post(url, headers=headers, params=params, json=payload)
    resp.raise_for_status()
    out = resp.json()
    text = out["candidates"][0]["content"]["parts"][0]["text"]
    job["keywords"] = text
    return job

def main(input_path: str):
    api_key = os.environ["GEMINI_API_KEY"]
    with open(input_path, encoding="utf-8") as f:
        jobs = json.load(f)

    for j in jobs:
        j = extract_for_job(j, api_key)

    with open(input_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    args = parser.parse_args()
    main(args.input)
