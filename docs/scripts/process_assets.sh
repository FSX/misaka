#/usr/bin/env bash

# Compile lesscss into CSS and compress it
lessc -x assets/screen.less assets/all.css
rm -r assets/*.less
