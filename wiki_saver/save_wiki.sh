#!/bin/bash

repo_list=${1}

while read line; 
do
  echo $line; 
  org=$(dirname $line) 
  mkdir -p ../wikis_${org}
  git clone git@github.com:${line}.wiki.git ../wikis_${line}
  echo "__________________________________________"
done < ${repo_list}

