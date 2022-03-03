#!/bin/bash

# Usage: bash ./clone_repos.sh file.csv CubitCodeReview
#                              <filename> <org_name>

INPUT=${1:-"file.csv"}
ORG=${2:-"org"}
OLDIFS=$IFS
IFS=';'
[ ! -f $INPUT ] && { echo "$INPUT file not found"; exit 99; }
while read name priv ssn tel status
do
	LINK="git@github.com:$ORG/$name.git"
	echo "Clone Repo : $LINK"
	git clone $LINK
	echo "__________________________________________"
done < $INPUT
IFS=$OLDIFS