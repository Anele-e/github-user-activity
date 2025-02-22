import json
import os
import requests
import sys
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_headers():
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        raise ValueError(
            "Provide github token in an environmental variable named GITHUB_TOKEN"
        )
    return {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json",
    }


def invalid_github_token(response):
    if response.status_code == 401:
        response_data = response.json()
        if "Bad Credentials" in response_data.get("message"):
            raise Exception("Invalid Github token")


def token_rate_limit(response):
    if response.status_code == 403:
        response_data = response.json()
        if "API rate limit exceeded" in response.get("message"):
            raise Exception("API rate limit exceeded")


def validate_username(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    if response.status_code == 404:
        raise ValueError(f"The username {username} does not exist")


def get_username():
    if len(sys.argv) < 2:
        raise ValueError("Missing username")
    username = sys.argv[1]
    return username


def get_structure(activity):
    output = ""
    user = activity["actor"]["login"]
    type = activity["type"]
    repo_name = activity["repo"]["name"]
    payload = activity["payload"]
    action = payload.get("action")
    if type == "CreateEvent":
        if payload["ref_type"] == "repository":
            output = f"Created a new repository {repo_name}"
        elif payload["ref_type"] == "branch":
            output = f"Created a new branch in {repo_name}"

    if type == "PushEvent":
        commit_count = len(payload["commits"])
        output = f"Pushed {commit_count} commits to {repo_name}"
    if type == "ForkEvent":
        forked_repo = payload["forkee"]["full_name"]
        output = f"forked {repo_name} to {forked_repo}"

    if type == "PullRequestEvent":
        if action == "open":
            output = f"Opened a pull request in {repo_name}"
        elif action == "closed":
            output = f"Closed a pull request in {repo_name}"
        elif action == "merged":
            output = f"Merged a pull request in {repo_name}"

    if type == "IssuesEvent":
        if action == "opened":
            output = f"Opened an issue in {repo_name}"
        elif action == "closed":
            output = f"Closed an issue in {repo_name}"
        elif action == "edited":
            output = f"Edited an issue in {repo_name}"

    if not output:
        output = f"Unhandled event type: {type} in repository {repo_name}"
    return output


def get_user_activity():

    output_list = []
    username = get_username()
    headers = get_headers()
    url = f"https://api.github.com/users/{username}/events"
    params = {"state": "all", "per_page": 100, "page": 1}

    validate_username(username)

    while True:
        activities = []
        response = requests.get(url, headers=headers, params=params)

        token_rate_limit(response)
        invalid_github_token(response)

        if response.status_code != 200:
            break
        activities = response.json()

        if not activities:
            break

        for activity in activities:
            output_list.append(get_structure(activity))
        params["page"] += 1
    for output in output_list:
        print(f"-{output}")


if __name__ == "__main__":
    get_user_activity()
