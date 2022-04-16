#!/bin/python3
# usage: python3 issues_backup.py --token <token_file> --repos <repos file>
import os

from github import Github
import argparse
import csv
from json import dump
import os.path as path


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, required=True,
                        dest='token',
                        help='github token')
    parser.add_argument('--repos', type=str, required=True,
                        dest='repos',
                        help='file w/repos list')
    results = parser.parse_args()
    return results


def get_token(filename):
    with open(filename) as file:
        token = file.readline().strip()
    return token


def get_repos(filename):
    repos = []
    with open(filename) as file:
        reader = csv.reader(file, delimiter=';', quotechar='|')
        next(reader, None)
        print("REPOS:")
        for row in reader:
            print(row[:1][0])
            repos.append(row[:1][0])
    return repos


def get_issue_info(issue):
    return {
        'id': issue.id,
        'title': issue.title,
        'assignees': [assignee.login for assignee in issue.assignees],
        'created_at': str(issue.created_at),
        'labels': [label.name for label in issue.get_labels()],
        'state': issue.state,
        'user': issue.user.login
    }


if __name__ == '__main__':
    args = parse_args()
    g = Github(get_token(args.token))
    org_name = args.repos.split('.')[0]
    if not path.exists(org_name):
        os.mkdir(org_name)
    for reponame in get_repos(args.repos):
        full_reponame = f"{org_name}/{reponame}"
        print('get {}'.format(full_reponame))
        repo = g.get_repo(full_reponame)
        issues = repo.get_issues(state='all')
        issues_info = []
        print('get issues')
        for issue in issues:
            issues_info.append(get_issue_info(issue))
        with open('{}/{}.issues.json'.format(org_name, reponame.replace('/', '--')), 'w') as file:
            dump(issues_info, file, ensure_ascii=False, indent=3)
