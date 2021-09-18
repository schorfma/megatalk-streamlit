for file in ingredients/*/*.svg
  do
    inkscape --without-gui "$file" --export-png="${file%.svg}.png"
  done
