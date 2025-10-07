#!/bin/bash

repo_list=${1}

while read line; 
do
  echo $line; 
  org=$(dirname $line) 
  mkdir -p ../wikis_${org}

  LINK="git@github.com:${line}.wiki.git"
  BACKUP_REPO_DIR=../wikis_${line}
  if [ ! -d "$BACKUP_REPO_DIR" ]; then
    git clone $LINK $BACKUP_REPO_DIR
  else
    echo "REPO WIKI $name ($BACKUP_REPO_DIR)  EXISTS. FETCHING."
    cd $BACKUP_REPO_DIR
    git fetch -a
    cd -
  fi
  echo "__________________________________________"
done < ${repo_list}

