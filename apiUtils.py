import subprocess
import json
import os
#import re

def load_session():
    """Load the session token from the environment if it exists."""
    for key, value in os.environ.items():
        if key.startswith("OP_SESSION_"):
            print(f"Session token found in environment: {key}")
            return key  # Return the key of the found session token
    print("No session token found in environment.")
    return None

def save_session(env_var, session):
    """Save the session token to the appropriate environment variable."""
    os.environ[env_var] = session
    print(f"Session token saved in environment variable: {env_var}")

def login_if_needed():
    # Attempt to check if logged in
    session_key = load_session()
    if session_key:
        try:
            # Check if the user is logged in using the session token
            subprocess.run(["op", "whoami"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            print("Already logged in.")
            return
        except subprocess.CalledProcessError:
            print("Session token invalid, logging in again...")
    # If the check fails, perform the login
    print("You are not logged in, performing login...")
    result = subprocess.run("op signin", shell=True, capture_output=True, text=True)

    # Check if signin was successful
    if result.returncode == 0:
        # Extract the session token using regex (account-specific environment variable)
        match = re.search(r'export (\S+)="(\S+)"', result.stdout)
        if match:
            env_var, value = match.groups()
            save_session(env_var, value)  # Save the session token to the appropriate environment variable
            #print(f"Login successful. Session token set as {env_var}.")
        else:
            print("Failed to parse the session token.")
    else:
        print("Login failed. Please check your credentials.")


def get_token(note_title):
    login_if_needed()
    print("Retrieving token...")

    try:
        result = subprocess.run(
            ['op', 'item', 'get', note_title, '--format', 'json'],
            capture_output=True,
            text=True,
            check=True
        )
        note_item = json.loads(result.stdout)

        if note_item['fields']:
            secure_note = note_item['fields'][0]['value']  # Adjust if necessary
            #print("Token retrieved.")
            return secure_note
        else:
            print("No fields found in the secure note.")
            return None

    except subprocess.CalledProcessError as e:
        print(f"Error fetching secure note: {e.stderr.strip()}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while fetching the note: {e}")
        return None