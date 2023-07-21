#!/bin/bash

# This script recursively deletes all files within specific subdirectories of "resources/images".
# By default, it excludes the "archive" directory unless the "-all" flag is used.
# You can run it from the root directory of the project with the following command:
# sh ./scripts/cleanup.sh

function recursive_delete() {
  for sub_dir in "$1"/*
  do
    if [ -d "$sub_dir" ]
    then
      if [ "$(ls -A $sub_dir)" ]; then
         echo "Deleting files in directory: $sub_dir"
         rm -r "$sub_dir"/*
      fi
      recursive_delete "$sub_dir"
    fi
  done
}

# Parse command-line arguments
while getopts ":all" opt; do
  case $opt in
    all)
      echo "Including deletion in archive" >&2
      include_archive=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

# Define the directories
directories=("facets" "head_shots" "process_me")

# Include the archive directory if the -all flag was used
if [ "$include_archive" = true ] ; then
    directories+=("archive")
fi

# Loop over the directories
for dir in "${directories[@]}"
do
  if [ "$dir" = "head_shots" ] && [ "$(ls -A resources/images/$dir)" ]; then
      echo "Deleting files in directory: resources/images/$dir"
      rm -r "resources/images/$dir"/*
  fi
  recursive_delete "resources/images/$dir"
done
