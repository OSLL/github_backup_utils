#!/bin/bash
set -e

BACKUP_DIR="../backups"

if [ ! -d "$BACKUP_DIR" ]; then
  mkdir "$BACKUP_DIR"
  echo "Folder $BACKUP_DIR created"
fi

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 N folder1 [folder2 ... folderN]"
  exit 1
fi

N=$1
shift
FOLDERS=("$@")


copy_folder() {
  local folder=$1
  local timestamp=$(date +"%Y_%m_%d_%H_%M")
  local new_folder_name="${folder}_${timestamp}"
  echo "Star copy $folder into $BACKUP_DIR/$new_folder_name"
  cp -r -f "$folder" "$BACKUP_DIR/$new_folder_name"
  echo "Folder $folder copied into $BACKUP_DIR/$new_folder_name"
}

for folder in "${FOLDERS[@]}"; do
  if [ -d "$folder" ]; then
    copy_folder "$folder"
  else
    echo "Folder $folder doesn't exist."
  fi
done

clean_old_copies() {
  local folder=$1
  local pattern="${folder}_*"
  local copies=("$BACKUP_DIR"/$pattern)
  # echo ${copies[@]}   # дебаг вывод чтобы посмотреть на то, как исщутся копии 

  if [ ${#copies[@]} -gt $N ]; then
    local num_to_delete=$(( ${#copies[@]} - N ))
    for ((i=0; i<num_to_delete; i++)); do
      echo "Started deleting ${copies[i]}"
      rm -rf "${copies[i]}"
      echo "Deleted old copy ${copies[i]}"
    done
  fi
}

for folder in "${FOLDERS[@]}"; do
  clean_old_copies "$folder"
done
