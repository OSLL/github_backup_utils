#!/bin/bash

# Requirements
# ./token - contains github token
# ./orgs - orgs list (separated with newline)

echo "Running export_org_repos.py"
python3 ./export_org_repos.py --token ./token --orgs ./orgs


echo "Cloning repos"

while IFS= read -r org; do
  echo "Processing $org"
  echo "Cloning repos of $org"
  ./clone_repos.sh $org.csv $org

  echo "Cloning wikis of $org"

  ../wiki_saver/csv_to_plain_list.sh $org.csv ${org}_list.txt ${org}
  ../wiki_saver/save_wiki.sh ${org}_list.txt

  echo "Backing up issues of $org"
  python3 ./issues_backup.py --token token --repos $org.csv --force
done <./orgs

read -n 1 -s -r -p "Press any key to continue"
