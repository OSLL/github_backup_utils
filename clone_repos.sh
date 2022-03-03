#!/bin/bash

# Usage: bash ./clone_repos.sh file.csv CubitCodeReview
#                              <filename> <org_name>

INPUT=${1:-"file.csv"}
ORG=${2:-"org"}
OLDIFS=$IFS
IFS=';'

if [ ! -d "$ORG" ]; then
  mkdir $ORG
fi

[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read name priv issues perms
do
	LINK="git@github.com:$ORG/$name.git"
    if [ ! -d "$name" ]; then
	    git clone $LINK
    else
      echo "REPO $name EXISTS. FETCHING."
      cd $name
      git fetch
      cd ..
    fi
	echo "__________________________________________"
done < $INPUT
IFS=$OLDIFS