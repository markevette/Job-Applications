# create_google_doc.py
import os
import json
import argparse

def main(jobs_path: str):
    service_account_json = os.environ["GOOGLE_SERVICE_ACCOUNT_JSON"]
    # TODO: build Google Docs client from service account
    with open(jobs_path, encoding="utf-8") as f:
        jobs = json.load(f)

    for j in jobs:
        # TODO: create doc, write j["tailored_resume"], store link
        j["google_doc_link"] = "https://docs.google.com/document/d/1SjDHcQNzgDbmxj-fXRY1pUoWvz646zzqUSFQe-w9iFc/edit?tab=t.0"

    with open(jobs_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--jobs", required=True)
    args = parser.parse_args()
    main(args.jobs)
