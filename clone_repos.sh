#!/bin/bash

# Usage: bash ./clone_repos.sh file.csv CubitCodeReview
#                              <filename> <org_name> [backup_dir=..]

INPUT=${1:-"file.csv"}
ORG=${2:-"org"}
BACKUP_DIR=${3:-".."}
BACKUP_ORG_DIR=$BACKUP_DIR/$ORG
OLDIFS=$IFS
IFS=';'


if [ ! -d "$ORG" ]; then
  mkdir -p $BACKUP_ORG_DIR
fi

dir=`pwd`

[ ! -f $INPUT ] && {
  echo "$INPUT file not found"
  exit 99
}
i=1
while read name archived has_issues has_wiki is_private; do
  if [ "$i" == '1' ]; then
    i=0
    continue # skip column's name
  fi
  if [ "$archived" == 'True' ]; then
    continue # skip archived repo
  fi
  LINK="git@github.com:$ORG/$name.git"
  $BACKUP_REPO_DIR=$BACKUP_ORG_DIR/$name
  if [ ! -d "$BACKUP_REPO_DIR" ]; then
    git clone $LINK $BACKUP_REPO_DIR
  else
    echo "REPO $name ($BACKUP_REPO_DIR)  EXISTS. FETCHING."
    cd $BACKUP_REPO_DIR
    git fetch -a
    cd $dir
  fi
  echo "__________________________________________"
done <$INPUT
IFS=$OLDIFS
