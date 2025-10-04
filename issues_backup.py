#!/bin/python3
# usage: python3 issues_backup.py --token <token_file> --repos <repos file>
import os

from github import Auth, Github, Issue
import argparse
import csv
from json import dump, load
import os.path as path
import glob
from time import sleep
from datetime import datetime
import pytz

utc = pytz.UTC

DELAY = 1  # Delay to avoiding reach of Github API limit


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--token", type=str, required=True, dest="token", help="file with github token"
    )
    parser.add_argument(
        "--repos", type=str, required=True, dest="repos", help="csv file w/repos list"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        required=False,
        dest="force",
        help="force rewrite issues",
    )
    results = parser.parse_args()
    return results


def get_checked_repos(path):
    res = []
    for file in glob.glob(glob.escape(path) + "/*.issues.json"):
        res.append(os.path.basename(file).split(".")[0])
    return res


def get_token(filename):
    with open(filename) as file:
        token = file.readline().strip()
    return token


def get_repos(filename):
    repos = []
    with open(filename) as file:
        reader = csv.DictReader(file, delimiter=";", quotechar="|")
        print("REPOS:")
        for row in reader:
            repos.append(
                (row["repo_name"], bool(int(row["archived"])), bool(int(row["has_issues"])))
            )
    return repos


def get_issue_info(issue: Issue.Issue):
    return {
        "id": issue.id,
        "title": issue.title,
        "assignees": [assignee.login for assignee in issue.assignees],
        "created_at": issue.created_at.strftime(r"%d.%m.%y %H:%M:%S"),
        "labels": [label.name for label in issue.get_labels()],
        "state": issue.state,
        "user": issue.user.login,
        "body": issue.body,
        "is_pr": bool(issue.pull_request)
    }


def get_issues_info(repo):
    return repo.get_issues(state="all")


if __name__ == "__main__":
    args = parse_args()
    g = Github(auth=Auth.Token(get_token(args.token)))
    org_name = args.repos.split(".")[0]
    checked_repos = []
    if not path.exists(org_name):
        os.mkdir(org_name)
    else:
        checked_repos = get_checked_repos(org_name)
    repos = get_repos(args.repos)

    for i, repo_item in enumerate(repos, start=1):
        reponame, is_archived, has_issues = repo_item
        print(
            f"Processing {i}/{len(repos)}: {reponame}, archived = {is_archived}, has_issues = {has_issues}"
        )
        if not has_issues:
            print(f"Skipping {reponame} (zero issues)...")
            continue
        elif is_archived:
            print(f"Skipping {reponame} (archived repo)...")
            continue
        elif (not args.force) and (reponame in checked_repos):
            print(f"Skipping {reponame} (backup exists)...")
            continue
        while True:
            try:
                full_reponame = f"{org_name}/{reponame}"
                print("Recieving data for {}".format(full_reponame))
                repo = g.get_repo(full_reponame)
                file_name = "{}/{}.issues.json".format(
                    org_name, reponame.replace("/", "--")
                )
                if path.exists(file_name):
                    repo_updated_at = repo.updated_at.replace(tzinfo=utc)
                    file_updated = datetime.fromtimestamp(
                        path.getmtime(file_name)
                    ).replace(tzinfo=utc)
                    print(
                        f"Repo {full_reponame} updated at {repo_updated_at}, file updated at {file_updated}"
                    )
                    if repo_updated_at < file_updated:
                        print(
                            f"Repo {full_reponame} does not have new changes, skipping"
                        )
                        break
                    else:
                        print(f"Repo {full_reponame} has new changes, need to backup")
                else:
                    print(f"File for repo {full_reponame} does not exist")
                issues = get_issues_info(repo)
                issues_info = []
                for issue in issues:
                    if not issue.pull_request:
                        # skip PR, that also in issues
                        issues_info.append(get_issue_info(issue))
                    sleep(DELAY)

                with open(file_name, "w") as file:
                    dump(issues_info, file, ensure_ascii=False, indent=3)

                break
            except Exception as e:
                ## Sleep 1h
                print("Got exception, will wait for 1h and continue")
                print(e)
                sleep(60 * 61)
                continue
        sleep(DELAY)
