#!/bin/python3
# usage: python3 export_org_repos.py --token <token_file> --github_nickname <your nickname> --orgs <organizations_file>
import argparse
from github import Github
import json
import csv
import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--token', type=str, required=True,
                        dest='token',
                        help='file w/github token')
    parser.add_argument('--github_nickname', type=str, required=True,
                        dest='github_nickname',
                        help='organization_names_file')
    parser.add_argument('--orgs', type=str, required=True,
                        dest='orgs',
                        help='organization_names_file')
    results = parser.parse_args()
    return results


def get_orgs(filename):
    with open(filename) as file:
        orgs = (org.strip() for org in file.readlines() if org.strip())
    return orgs


def get_writer_rows():
    return [
        "repo_name",
        "is_private",
        "issues_count",
        "permissions"
    ]


def get_repo_info(repo, org_name="", username=""):
    users = ""
    for u in repo.get_collaborators():
        params = {
            "accept": "application/vnd.github.v3+json"
        }
        res = requests.get(f"https://api.github.com/repos/{org_name}/{repo.name}/collaborators/{u.login}/permission", params=params, auth=(username, args.token))
        users += f"{u.login}:{json.loads(res.text)['permission']},"
    return [
        str(repo.name),
        str(repo.private),
        str(len(list(repo.get_issues(state='all')))),
        str(users)
    ]


if __name__ == '__main__':
    args = parse_args()
    g = Github(args.token)
    for org_name in get_orgs(args.orgs):
        print('get org [{}]'.format(org_name))
        org = g.get_organization(org_name)
        org_repos = org.get_repos()
        with open(f'{org_name}.csv', 'w') as file:
            writer = csv.writer(file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(get_writer_rows())
            for repo in org_repos:
                print(f"Handling repo [{repo.name}]")
                info = get_repo_info(repo, org_name, args.github_nickname)
                writer.writerow(info)