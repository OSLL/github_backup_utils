#!/bin/python3
import sys
import requests
from github import Github


def main(token, repo_name):
    g = Github(token)
 

    repo = g.get_repo(repo_name)
    print(repo.name)
    print("PR URL;PR_NAME;author;merged_by")
    pulls = repo.get_pulls(state="closed")
    for pull in pulls:
        if pull.merged:
            print("https://github.com/{}/pull/{};{};{};{}".format(repo_name, pull.number, pull.title, pull.user.login, pull.merged_by.login))


if __name__ == "__main__":
    token = sys.argv[1]
    repo = sys.argv[2]
    print(token)
    main(token, repo)
