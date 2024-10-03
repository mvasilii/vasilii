#!/bin/bash

cd /home/vasilii.mikhailov/aiven_git/aiven/aiven-core
git fetch --all
git checkout main
git pull origin main
make build-dep-fedora
make
