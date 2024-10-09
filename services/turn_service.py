import subprocess
import json
import os
import sys
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import apiUtils


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

    # Retrieve token
    note_title = "AVN client token"
    token = apiUtils.get_token(note_title)
       
    service_list = get_services(services_file)
    print(service_list)
    for service in service_list:
            service = service.strip()  # Remove any trailing whitespace or newlines
            if service:
                print(project, service, power_on)
                # Commented out for dry-run
                apiUtils.update_service_power(token, project, service, power_on)


if __name__ == "__main__":
    main()