#!/usr/bin/env bash

echo "...updating repository from server..."
git reset --hard
git config pull.rebase true
git pull

echo "...activating conda env..."
conda activate crome-env

if [ $# -eq 0 ]
  then
    source run.sh
else
    source run.sh "$@"
fi