import json
import argparse

def main(input_path: str, output_path: str, roles: list[str]):
    with open(input_path, encoding="utf-8") as f:
        jobs = json.load(f)

    roles_lower = [r.lower() for r in roles]
    filtered = [
        j for j in jobs
        if any(r in j.get("title", "").lower() for r in roles_lower)
    ]
    filtered = sorted(filtered, key=lambda j: j.get("datePosted", ""), reverse=True)[:5]

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(filtered, f, indent=2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--roles", required=True,
                        help="Comma-separated roles")
    args = parser.parse_args()
    roles = [r.strip() for r in args.roles.split(",") if r.strip()]
    main(args.input, args.output, roles)
