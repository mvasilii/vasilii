# BEGIN AIVENRC BLOCK
# Aiven specific section
[[ -f ${HOME}/.aiven/rc.sh ]] && source "${HOME}"/.aiven/rc.sh
# END AIVENRC BLOCK

# Save multi-session history
setopt APPEND_HISTORY
setopt INC_APPEND_HISTORY

# Share history between sessions
setopt SHARE_HISTORY

# Ensure commands are written to history immediately
setopt HIST_IGNORE_SPACE  # Ignore commands that start with a space
setopt HIST_REDUCE_BLANKS  # Remove extra spaces from the history

# Set history file and size
HISTFILE=~/.zsh_history
HISTSIZE=1000
SAVEHIST=2000

# Load GPG key
echo ""
echo "Loading GPG Key" 
echo ""

gpgconf --kill gpg-agent
gpg-agent --daemon
echo "Hello" | gpg --sign --local-user "${AIVEN_USER_NAME:-$(whoami)}@aiven.io" --recipient "${AIVEN_USER_NAME:-$(whoami)}@aiven.io" --encrypt | gpg --decrypt
cd ~/aiven_git/aiven/aiven-core

export OP_SESSION_3VO7TQQYQ5C43A4AD7Y7BDI5H4="EXXuYhGWbH5kfflQZ7VAMgzCE1AXjmNdHisKqWV3eF4"
