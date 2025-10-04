#!/bin/bash

# Transforms CSV list of repos (w/has_wiki flag) to plain list in format (only repos w/has_wiki=1):
# org/repo


src=${1} # Source file (csv)
dst=${2} # Destination file (plain text)
org=${3} # Organization

tail -n +2 "${src}" | awk -F';' '$4 == "1" {print "'"${org}"'/"$1}' > ${dst}
