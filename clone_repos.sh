#!/bin/bash

# Usage: bash ./clone_repos.sh file.csv CubitCodeReview
#                              <filename> <org_name>

INPUT=${1:-"file.csv"}
ORG=${2:-"org"}
OLDIFS=$IFS
IFS=';'

if [ ! -d "$ORG" ]; then
  mkdir -p $ORG
fi

dir=`pwd`

[ ! -f $INPUT ] && {
  echo "$INPUT file not found"
  exit 99
}
i=1
while read name priv issues perms; do
  if [ "$i" == '1' ]; then
    i=0
    continue # skip column's name
  fi
  LINK="git@github.com:$ORG/$name.git"
  if [ ! -d "$ORG/$name" ]; then
    git clone $LINK $ORG/$name
  else
    echo "REPO $name (`pwd`/$ORG/$name)  EXISTS. FETCHING."
    cd $ORG/$name
    git fetch -a
    cd $dir
  fi
  echo "__________________________________________"
done <$INPUT
IFS=$OLDIFS
