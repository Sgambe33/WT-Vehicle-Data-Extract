import json
import subprocess
from datetime import datetime

def read_updates(file_path):
    """Read the updates.json file and return the list of (commit SHA, date string) tuples sorted chronologically."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            updates = json.load(f)
        commits = [
            (update["commithash"], update["date"])
            for update in updates
            if "commithash" in update and "date" in update
        ]
        commits.sort(key=lambda x: datetime.strptime(x[1], "%d-%m-%Y"))
        return commits
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []

def checkout_commit(commit_sha):
    """Checkout a specific commit using Git."""
    try:
        subprocess.run(
            ["git", "checkout", commit_sha[0], "--force"],
            check=True,
            text=True,
            cwd="D:\\War-Thunder-Datamine"
        )
        print(f"Checked out commit: {commit_sha}")
    except subprocess.CalledProcessError as e:
        print(f"Error checking out commit {commit_sha}: {e}")

def run_main():
    """Run main.py using Python."""
    try:
        subprocess.run([".\\.venv\\Scripts\\python.exe", "main.py"], check=True, text=True)
        print("main.py executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error running main.py: {e}")

def main():
    updates_file = "./utils/updates.json"
    commits = read_updates(updates_file)

    if not commits:
        print("No commits found in updates.json.")
        return

    start_date_str = "10-06-2023"
    start_date = datetime.strptime(start_date_str, "%d-%m-%Y")

    filtered_commits = [
        commit for commit in commits
        if datetime.strptime(commit[1], "%d-%m-%Y") > start_date
    ]

    if not filtered_commits:
        print(f"No commits found after {start_date_str}.")
        return

    for commit_sha in filtered_commits:
        checkout_commit(commit_sha)
        run_main()

if __name__ == "__main__":
    main()
