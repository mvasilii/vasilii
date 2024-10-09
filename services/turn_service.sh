#!/bin/zsh
# This script checks if the NFS fileshare is mounted and accessible. 
# It also tries to autorecover the NFS fileshare by automounting the folder.
# Usage: bash turn_services.sh on/off
#

# Source the .zshrc file to load aliases
#[[ -f ~/.aiven/rc.sh ]] && source ~/.aiven/rc.sh
alias avn-prod='python3 -m aiven.admin --config op://private/aivendb_readonly/notesPlain'


# Check argument
[[ $# -ne 1 ]] && {
  echo "Usage: bash `basename $0` <on/off>"
  echo "Example: bash `basename $0` on"
  die "Incorrect use" 1
}

# Get the directory where the script is located
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")

# Set the path to services.txt in the same folder as the script
fs="$SCRIPT_DIR/services_id.txt"
#fs="services_id.txt"
#echo "Current PATH: $PATH"
#fs="/home/vasilii.mikhailov/aiven_git/aiven/vasilii/services/services_id.txt"
# Check if services.txt exists
if [[ ! -f "$fs" ]]; then
  echo "File $fs not found. Please ensure it exists in the same directory as the script."
  exit 1
fi

cd /home/vasilii.mikhailov/aiven_git/aiven/aiven-core
# Array to store services
services=()

# Function to load lines from file into array
load_services_to_array() {
  local file="$1"
  if [[ -f "$file" ]]; then
    while IFS= read -r line; do
      services+=("$line")  # Add each line to the services array
    done < "$file"
  else
    die "File $file not found." 1
  fi
}

main(){
  # Load services from the file
  load_services_to_array "$fs"

  # Enter pass for 1 password
  # eval $( op signin )
  # Process based on input (on/off)
  case "$1" in
    on)
      msg "Turning services on."
      for service in "${services[@]}"; do
        msg "Turning on service: $service"
        avn-prod service poweron $service --customer-reason "API test" --yes
      done
      ;;
    off)
      msg "Turning services off."
      for service in "${services[@]}"; do
        msg "Turning off service: $service"
        avn-prod service poweroff $service --customer-reason "API test" --yes
      done
      ;;
    *)
      die "Invalid argument. Use 'on' or 'off'." 1
      ;;
  esac
  die "Done." 0
}

msg() {
  echo >&2 -e "Aiven Services Turn On/Off: ${1-}"
  logger "Aiven Services Turn On/Off: $1"
}

die() {
  local msg=$1
  local code=${2-1} # default exit status 1
  msg "$msg"
  exit "$code"
}

main "$1"