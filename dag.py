import os
import subprocess
from github import Github
import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime

def get_github_repo_name():
    remote_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"]).decode("utf-8").strip()
    remote_url_parts = remote_url.split("/")
    repo_name = remote_url_parts[-1].split(".")[0]
    username = remote_url_parts[-2].split(":")[-1]
    return f"{username}/{repo_name}"

access_token = os.environ["GITHUB_TOKEN"]
g = Github(access_token)

repo_name = get_github_repo_name()
repo = g.get_repo(repo_name)

issues = repo.get_issues(state="all", labels=["bug"])

daily_issue_count = defaultdict(int)
for issue in issues:
    created_at = issue.created_at.date()
    daily_issue_count[created_at] += 1

dates = sorted(daily_issue_count.keys())
counts = [daily_issue_count[date] for date in dates]

cumulative_counts = [sum(counts[:i+1]) for i in range(len(counts))]

plt.plot(dates, cumulative_counts, marker='o')
plt.xlabel('Date')
plt.ylabel('Number of Defects')
plt.title(f'Defect Arrival Graph for {repo_name}')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
