#!/bin/zsh

sudo systemctl restart chronyd
cd $AIVEN_CORE_PATH
git fetch --all
git checkout main
git pull origin main
make build-dep-fedora
make
#aprod prod checkout-prod
#avn-admin prod checkout-prod
