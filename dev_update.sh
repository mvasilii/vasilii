#!/bin/bash

cd $AIVEN_CORE_PATH
git fetch --all
git checkout main
git pull origin main
make build-dep-fedora
make
