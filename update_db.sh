#!/bin/bash

cd x86_64

if which repo-add; then
  rm -rf *.tar.gz
  repo-add --remove packages-aeros-gnome45.db.tar.gz *.pkg.tar.zst
else
  echo "This system is not Arch!"
  exit 1
fi
