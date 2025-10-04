#!/bin/python3
# usage: python3 export_org_repos.py --token <token_file> --orgs <organizations_file>
import argparse
from github.Repository import Repository
import csv
from json import dump as json_dump
from time import sleep
from utils import get_github_client


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--token", type=str, required=True, dest="token", help="file w/github token"
    )
    parser.add_argument(
        "--orgs", type=str, required=True, dest="orgs", help="organization_names_file"
    )
    parser.add_argument(
        "--verbose", action="store_true", dest="verbose", help="verbose result"
    )
    results = parser.parse_args()
    return results


def get_orgs(filename):
    with open(filename) as file:
        orgs = (org.strip() for org in file.readlines() if org.strip())
    return orgs


def get_writer_rows(verbose=False):
    headers = "repo_name,archived,has_issues,has_wiki,is_private,last_pushed_at,size,pr_count,issues_count,users_count,permissions".split(
        ","
    )
    return headers if verbose else headers[:5]


def get_repo_info(repo: Repository, verbose=False):
    info = {
        "repo_name": repo.name,
        "is_private": int(repo.private),
        "archived": int(repo.archived),
        "has_wiki": int(repo.has_wiki),
        "has_issues": int(repo.has_issues),
    }
    if verbose:
        users = ""
        try:
            users_info = repo.get_collaborators()
            users_count = users_info.totalCount
            for u in users_info:
                users += f"{u.login}:{str(u.permissions)},"
        except Exception as exc:
            print(f"Error getting collaborators: {exc}")

        pr_count, issues_count = 0, 0
        if repo.has_issues:
            all_issues = list(
                repo.get_issues(state="all")
            )  # TODO: use totalCount after release
            issues_count = sum(not issue.pull_request for issue in all_issues)
            pr_count = len(all_issues) - issues_count

        info.update(
            {
                "last_pushed_at": repo.pushed_at.strftime(r"%d.%m.%y %H:%M:%S"),
                "size": repo.size,
                "pr_count": pr_count,
                "issues_count": issues_count,
                "users_count": users_count,
                "permissions": users,
            }
        )
    return info


if __name__ == "__main__":
    args = parse_args()
    g = get_github_client(args.token)

    orgs_data = {}

    for org_name in get_orgs(args.orgs):
        print(f"get org [{org_name}]")
        orgs_data[org_name] = []
        org = g.get_organization(org_name)

        with open(f"{org_name}.csv", "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=get_writer_rows(args.verbose),
                delimiter=";",
                quotechar="|",
                quoting=csv.QUOTE_MINIMAL,
            )
            writer.writeheader()

            repos = org.get_repos()
            for repo in repos:
                print(f"Handling repo [{repo.name}]")
                info = get_repo_info(repo, args.verbose)
                orgs_data[org_name].append(info)
                writer.writerow(info)
                sleep(0.1)

    if args.verbose:
        with open("orgs_info.json", "w", encoding="utf-8") as file:
            json_dump(orgs_data, file, ensure_ascii=False, indent=4)
