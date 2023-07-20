#!/bin/bash

directory="/Users/santiagotorres/Documents/touchdesigner projects/facedetector/images/processme"

# Navegar al directorio
cd "$directory" || exit

# Iterar sobre los archivos en el directorio
for file in *; do
  # Obtener el nombre del archivo sin la extensión
  filename="${file%.*}"
  
  # Obtener la extensión del archivo
  extension="${file##*.}"
  
  # Renombrar el archivo eliminando el nombre desde la primera aparición de "OK"
  new_filename="${filename#*OK}.$extension"
  
  # Renombrar el archivo
  mv "$file" "$new_filename"
done
