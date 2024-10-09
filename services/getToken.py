import subprocess
import json
import os
import sys
import requests

# Function to authenticate with 1Password and get session
def authenticate_1password():
    try:
        # Run the `op signin` command and capture the result
        result = subprocess.run(
            ['op', 'signin'],
            capture_output=True,
            text=True,
            shell=True
        )

        # Check if the signin command was successful
        if result.returncode != 0:
            print("Error during 1Password sign-in:", result.stderr)
            return None

        # Parse the environment variable from the output (eval $(op signin) equivalent)
        output_lines = result.stdout.splitlines()
        for line in output_lines:
            if line.startswith("export"):
                # Extract and set the environment variable
                key_value = line.replace("export ", "").split("=")
                os.environ[key_value[0]] = key_value[1].strip('"')

        print("Authenticated successfully.")
        return True

    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        return False

# Function to get a secure note from 1Password
def get_secure_note(note_title):
    try:
        # Run the 1Password CLI command to fetch the secure note
        result = subprocess.run(
            ['op', 'item', 'get', note_title, '--format', 'json'],
            capture_output=True,
            text=True
        )

        # Check if the command was successful
        if result.returncode != 0:
            print("Error fetching secure note:", result.stderr)
            return None

        # Parse the JSON output
        note_item = json.loads(result.stdout)

        # Extract the note content safely
        if note_item['fields']:
            secure_note = note_item['fields'][0]['value']  # Adjust index as necessary
            print("Token retrieved.")
            return secure_note
        else:
            print("No fields found in the secure note.")
            return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def update_service_power(token, project, service, power_on):
    url = f"https://api.aiven.io/v1/project/{project}/service/{service}"
    headers = {
        "Authorization": f"Bearer {os.getenv('AIVEN_API_TOKEN')}",
        "Content-Type": "application/json"
    }
    data = {"powered": power_on}

    response = requests.patch(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print(f"Service {service} power updated successfully.")
    else:
        print(f"Failed to update service power. Status code: {response.status_code}, Response: {response.text}")

# Function to read services from a file and execute an API request for each line
def get_services(services_file):
    try:
        # Open and read the file line by line
        with open(services_file, 'r') as file:
            services = file.readlines()
            return services
    except FileNotFoundError:
        print(f"Error: {services_file} not found.")
    except Exception as e:
        print(f"An error occurred while sending API requests: {e}")


# Main function to handle authentication and note retrieval
def main():
    if len(sys.argv) != 2 or sys.argv[1] not in ["on", "off"]:
        print("Usage: python script.py [on|off]")
        sys.exit(1)

    option_arg = sys.argv[1]  # Get the option ('on' or 'off')
    # Map 'on' to True and 'off' to False
    power_on = True if option_arg == "on" else False
    services_file = 'services_name.txt'
    # Get the directory of the current script
    script_directory = os.path.dirname(os.path.abspath(__file__))
    services_file = os.path.join(script_directory, services_file)
    project = "dev-sandbox"
    #authenticate_1password()

    note_title = "AVN client token"
    # Authenticate with 1Password
    if authenticate_1password():
        # Get the secure note after successful authentication
        token = get_secure_note(note_title)
        #if token:
        #    #print("Secure Note Content:", token)
        #    print(token)
        #else:
        #    print("Failed to retrieve the secure note.")
    else:
        print("Authentication failed.")

    print("token:", token)
       
    service_list = get_services(services_file)
    print(service_list)
    for service in service_list:
            service = service.strip()  # Remove any trailing whitespace or newlines
            if service:
                print(token, project, service, power_on)
                #update_service_power(token, project, service, power_on)


if __name__ == "__main__":
    main()