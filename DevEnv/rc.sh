#!/usr/bin/env bash

# Allow substitution in the prompt each time it is rendered
setopt promptsubst

# Ignore history when the command stats with a space.
# Useful in case you need to pass passwords in env variables in the command line
setopt HIST_IGNORE_SPACE

# Set Aiven variables
export AIVEN_HOME="${HOME}/aiven_git/aiven"
export AIVEN_CORE_PATH="${HOME}/aiven_git/aiven/aiven-core"
export AIVEN_CONTAINER_PREFIX=aiven-fedora
export AIVEN_DEFAULT_RELEASE=35
export AIVEN_DEV_CLOUD="google-europe-west1"
export AIVEN_RPM_BUILD_PATH="/tmp/aiven-rpms"

# 1password aliases
alias opl='op whoami > /dev/null 2>&1 || eval $(op signin)'

# Project aliases
alias ahome='cd ${AIVEN_HOME}'
alias acore='cd ${AIVEN_CORE_PATH}'

# Development aliases
alias avn-dev='python3 -m aiven.admin dev'

# Production aliases
#alias AVN-PROD='python3 -m aiven.admin --config gopass:aiven/aivenprod/config.json --operator-config gopass:aivenprod-operator.json --sky aiven'
alias AVN-PROD='opl; python3 -m aiven.admin --config op://private/aivendb_readonly/notesPlain'
alias OVH-PROD='python3 -m aiven.admin --config gopass:ovh/ovhprod/config.json --operator-config gopass:ovhprod-operator.json --sky ovh'
alias avn-adminapi='python3 -m aiven.rest.admin.cli --api-production'

# User aliases
alias adminapi='avn-adminapi'
alias aapi='avn-adminapi'
alias AVN-ADMINAPI='avn-adminapi'
alias aprod='AVN-PROD'
alias avn-prod='AVN-PROD'

# avnpkg
# https://github.com/aiven/aiven-core/blob/0168b69edaf4ac9ea6dc812302bd6d32151c0a4d/avnpkg/README.md
alias avnpkg='/opt/avnpkg-venv/bin/avnpkg'

# Fixing zsh
alias shopt='/usr/bin/shopt'

# Set Python path
export PYTHONPATH="${PYTHONPATH:-}:${AIVEN_CORE_PATH}"

[[ -f ${HOME}/.aiven/functions.sh ]] && source "${HOME}"/.aiven/functions.sh

[ -x "$(command -v register-python-argcomplete)" ] && eval "$(register-python-argcomplete avn)"
