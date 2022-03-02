#!/bin/python3
# usage: python3 export_org_repos.py --token <token_file> --orgs <organizations_file>
import argparse
from github import Github
from json import dump
import csv

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, required=True,
                        dest='token',
                        help='file w/github token')
    parser.add_argument('--orgs', type=str, required=True,
                        dest='orgs',
                        help='organization_names_file')
    results = parser.parse_args()
    return results


def get_token(filename):
    with open(filename) as file:
        token = file.readline()
    return token


def get_orgs(filename):
    with open(filename) as file:
        repos = (repo.strip() for repo in file.readlines() if repo.strip())
    return repos


def get_repo_info(repo):
    return [
        str(repo.name),
        str(repo.id)
    ]


if __name__ == '__main__':
    args = parse_args()
    g = Github(get_token(args.token))
    for org_name in get_orgs(args.orgs):
        print('get org [{}]'.format(org_name))
        org = g.get_organization(org_name)
        org_repos = org.get_repos()
        with open(f'{org_name}.csv', 'w') as file:
            writer = csv.writer(file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for repo in org_repos:
                info = get_repo_info(repo)
                writer.writerow(info)
        #dump(issues_info, file, ensure_ascii=False, indent=3)
        # issues = repo.get_issues(state='all')
        # issues_info = []
        # print('get issues')
        # for issue in issues:
        #     issues_info.append(get_issue_info(issue))
        # with open('{}.issues.json'.format(reponame.replace('/', '--')), 'w') as file:
        #     dump(issues_info, file, ensure_ascii=False, indent=3)