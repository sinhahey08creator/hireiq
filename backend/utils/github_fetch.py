"""
Fetches a candidate's public GitHub activity using the free GitHub REST API.
No authentication needed for basic public data (rate-limited but fine for a demo).
"""

import requests


def get_github_summary(username: str) -> str:
    if not username:
        return ""

    try:
        user_resp = requests.get(f"https://api.github.com/users/{username}", timeout=5)
        if user_resp.status_code != 200:
            return "GitHub profile not found or username invalid."

        repos_resp = requests.get(
            f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10",
            timeout=5,
        )
        user_data = user_resp.json()
        repos_data = repos_resp.json() if repos_resp.status_code == 200 else []

        repo_lines = []
        for repo in repos_data[:5]:
            repo_lines.append(
                f"- {repo['name']}: {repo.get('description') or 'No description'} "
                f"(Language: {repo.get('language') or 'N/A'}, "
                f"Stars: {repo.get('stargazers_count', 0)}, "
                f"Last updated: {repo.get('updated_at')})"
            )

        summary = (
            f"Public Repos: {user_data.get('public_repos', 0)}\n"
            f"Followers: {user_data.get('followers', 0)}\n"
            f"Recent Repositories:\n"
            + ("\n".join(repo_lines) if repo_lines else "No public repositories found.")
        )
        return summary

    except Exception as e:
        return f"Could not fetch GitHub data: {str(e)}"
