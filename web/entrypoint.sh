#!/usr/bin/env bash

echo "...updating repository ..."
pwd
git reset --hard HEAD
git clean -f
git pull

echo "...launching server..."

python3 webapp.py