#!/usr/bin/env bash

echo "...updating repository from server..."
pwd
git reset --hard HEAD
git clean -f
git pull

if [ $# -eq 0 ]
  then
    source run.sh
else
    source run.sh "$@"
fi