#!/bin/python3
# usage: python3 issues_backup.py --token <token_file> --repos <repos file>
from github import Github
import argparse
from json import dump


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, required=True,
                        dest='token',
                        help='file w/github token')
    parser.add_argument('--repos', type=str, required=True,
                        dest='repos',
                        help='file w/repos list')
    results = parser.parse_args()
    return results


def get_token(filename):
    with open(filename) as file:
        token = file.readline()
    return token


def get_repos(filename):
    with open(filename) as file:
        repos = (repo.strip() for repo in file.readlines() if repo.strip())
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
    for reponame in get_repos(args.repos):
        print('get {}'.format(reponame))
        repo = g.get_repo(reponame)
        issues = repo.get_issues(state='all')
        issues_info = []
        print('get issues')
        for issue in issues:
            issues_info.append(get_issue_info(issue))
        with open('{}.issues.json'.format(reponame.replace('/', '--')), 'w') as file:
            dump(issues_info, file, ensure_ascii=False, indent=3)
