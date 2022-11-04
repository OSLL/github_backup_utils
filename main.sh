#!/bin/bash

# Requirements
# ./token - contains github token
# ./username - contains github username (token owner)
# ./orgs - orgs list (separated with newline)

echo "Running export_org_repos.py"
python3 ./export_org_repos.py --token ./token --github_nickname `cat ./username` --orgs ./orgs

echo "Cloning repos"

while read orgs; do
  echo $org
  ./clone_repos.sh $org.csv $org
done <./orgs
