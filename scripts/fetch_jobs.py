import os
import json
import argparse
import requests

def main(output_path: str):
    api_token = os.environ["APIFY_API_TOKEN"]
    # TODO: replace with your actual Apify actor/task URL
    url = "https://api.apify.com/v2/actor-tasks/evettemark~linkedin-jobs-actor-task/run-sync-get-dataset-items"
    params = {"token": api_token}
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    main(args.output)
