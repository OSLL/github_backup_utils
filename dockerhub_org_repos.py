#!/bin/python3
# usage: python3 issues_backup.py --cred <credential_file> --repos <repos_file>
# - credential_file is:
#   username
#   password
# - repos_file - filename: OSLL.* 
import argparse
import json
import os.path as path
import os
import sys
from json import dump

import requests


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--cred', type=str, required=True,
                        dest='cred',
                        help='file w/dockerhub credentials')
    parser.add_argument('--repos', type=str, required=True,
                        dest='repos',
                        help='file w/repos list')
    results = parser.parse_args()
    return results


def get_credentials(filename):
    with open(filename) as file:
        username = file.readline().strip()
        password = file.readline().strip()
    return username, password


def get_repos(filename):
    with open(filename) as file:
        repos = (repo.strip() for repo in file.readlines() if repo.strip())
    return repos


def login(username, password):
    response = requests.post(
        'https://hub.docker.com/v2/users/login/',
        headers={'Content-type': 'application/json'},
        data=json.dumps({
            'username': username,
            'password': password,
        }),
    )

    if not response.ok:
        sys.stderr.write("Login failed: %s\n" % response.text['detail'])
        sys.exit(1)

    return response.json()['token']


def get_repo_images(namespace, reponame, token):
    return requests.get(
        f'https://hub.docker.com/v2/namespaces/{namespace}/repositories/{reponame}/images',
        headers={'Authorization': 'JWT %s' % token},
    )


def main():
    args = parse_args()
    token = login(*get_credentials(args.cred))
    org_name = args.repos.split('.')[0]
    if not path.exists(org_name):
        os.mkdir(org_name)
    for reponame in get_repos(args.repos):
        image_info = get_repo_images(org_name, reponame, token).json()
        print(org_name, reponame, reponame, image_info)
        with open('{}/{}.json'.format(org_name, reponame.replace('/', '--')), 'w') as file:
            dump(image_info, file, ensure_ascii=False, indent=3)

if __name__ == "__main__":
    main()
