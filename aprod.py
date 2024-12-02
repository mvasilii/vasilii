import subprocess
import argparse
import json


def run_command(command):
    """Execute a shell command and return the output."""
    try:
        # Run the command and capture the output.
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout, None  # Return output and no error
    except subprocess.CalledProcessError as e:
        return None, e.stderr  # Return no output and error

def parse_json_output(output):
    """Parse the JSON output and return the corresponding Python object."""
    try:
        # Parse the output as JSON
        return json.loads(output), None
    except json.JSONDecodeError as e:
        return None, f"Failed to parse JSON: {e}"
    
def main(args):
    # Command to check whoami and sign in to OP if needed
    whoami_command = "op whoami > /dev/null 2>&1 || eval $(op signin)"
    # Execute the command in a shell context
    output, error = run_command(["bash", "-c", whoami_command])
    
    if error:
        print(f"Error during authentication: {error}")
    else:
        print("Authenticated successfully.")
    
    admin_api_alias = [
      "python3", "-m", "aiven.rest.admin.cli", "--api-production", "--json"
    ]

    aprod_alias = [
        "python3", "-m", "aiven.admin", "--config op://private/aivendb_readonly/notesPlain"
    ]
    
    # Now run the main command
    #logs_command = admin_api_alias + [
    #    "service", 
    #    "logs", 
    #    "system", 
    #    "575555", 
    #    "--since", "2024-11-18T06:00", 
    #    "--until", "2024-11-18T06:05"
    #]
    
    command_to_run = admin_api_alias + args

    output, error = run_command(command_to_run)
    if error:
        print("Error from api command:\n", error)
        return
  # Parse the JSON output
    json_output, parse_error = parse_json_output(output)
    if parse_error:
        print(parse_error)
    #else:
    #    print("Parsed JSON Output:\n", json.dumps(json_output, indent=4))

    # Check if the parsed JSON has "service_id" and print its value
    service_id = json_output.get('service_id')
    if service_id is not None:
        print(f"Service ID: {service_id}")
    else:
        print("No 'service_id' found in the output.")

    aprod_command = aprod_alias + [
        "service", 
        "describe", 
        str(service_id)
    ]

    output, error = run_command(aprod_command)
    if output:
        print("Output from aprod command:\n", output)
    if error:
        print("Error from aprod command:\n", error)

    
if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run Aiven service logs command.')
    # Allow any arguments after the script name, which will be passed to main()
    parser.add_argument('args', nargs=argparse.REMAINDER, help='Additional arguments for the logs command.')

    # Parse the arguments
    parsed_args = parser.parse_args()

    main(parsed_args.args)

