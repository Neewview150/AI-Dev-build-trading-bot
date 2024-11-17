import requests
import os
import sys
import argparse

def create_pull_request(repo_name, head_branch, base_branch, title, body):
    """
    Create a pull request on GitHub.
    
    :param repo_name: The repository name in the format 'owner/repo'.
    :param head_branch: The name of the branch where your changes are implemented.
    :param base_branch: The name of the branch you want the changes pulled into.
    :param title: The title of the pull request.
    :param body: The body text of the pull request.
    """
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set.")
        sys.exit(1)

    url = f"https://api.github.com/repos/{repo_name}/pulls"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": title,
        "head": head_branch,
        "base": base_branch,
        "body": body
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("Pull request created successfully.")
        print("URL:", response.json().get('html_url'))
    else:
        print("Failed to create pull request.")
        print("Response:", response.json())

def main():
    parser = argparse.ArgumentParser(description='Create a GitHub pull request.')
    parser.add_argument('repo_name', help='Repository name in the format "owner/repo".')
    parser.add_argument('head_branch', help='Branch name with your changes.')
    parser.add_argument('base_branch', help='Branch to merge changes into.')
    parser.add_argument('title', help='Title of the pull request.')
    parser.add_argument('body', help='Body of the pull request.')

    args = parser.parse_args()

    create_pull_request(
        repo_name=args.repo_name,
        head_branch=args.head_branch,
        base_branch=args.base_branch,
        title=args.title,
        body=args.body
    )

if __name__ == "__main__":
    main()
