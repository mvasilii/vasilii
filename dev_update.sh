#!/bin/zsh

sudo systemctl restart chronyd
op whoami > /dev/null 2>&1 || eval $(op signin)
cd $AIVEN_CORE_PATH
git fetch --all
git checkout main
git pull origin main
make build-dep-fedora
make
#aprod prod checkout-prod
python3 -m aiven.admin --config op://private/aivendb_readonly/notesPlain prod checkout-prod
