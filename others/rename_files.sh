#!/bin/bash

directory="./images/process_me"

cd "$directory" || exit

for file in *; do
  filename="${file%.*}"
  
  extension="${file##*.}"
  
  new_filename="${filename#*OK}.$extension"
  
  mv "$file" "$new_filename"
done
