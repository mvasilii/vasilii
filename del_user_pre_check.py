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
    
def main(email, org):
    # Command to check whoami and sign in to OP if needed
    #whoami_command = "op whoami > /dev/null 2>&1 || eval $(op signin)"
    # Execute the command in a shell context
    #output, error = run_command(["bash", "-c", whoami_command])
    
    #if error:
    #    print(f"Error during authentication: {error}")
    #else:
    #    print("Authenticated successfully.")
    
    admin_api_alias = [
      "python3", "-m", "aiven.rest.admin.cli", "--api-production", "--json"
    ]
    
    user_data = {}

    # 1. check Organization to get Account_ID
    # aapi organization describe org4f66f413a78
    print("Checking Account from the Organization " + str(org) + "...")
    account_command = admin_api_alias + ["organization", "describe", str(org), "--json"]

    output, error = run_command(account_command)
    if error:
        print("Error from api command:\n", error)
        return
    
  # Parse the JSON output
    json_output, parse_error = parse_json_output(output)
    if parse_error:
        print(parse_error)
    #else:
    #    print("Parsed JSON Output:\n", json.dumps(json_output, indent=4))
   
    # Check if the parsed JSON has "account_id" and print its value
    account_id = json_output.get('root_account', {}).get('account_id', '')
    if account_id is not None:
        #print(f"Account ID: {account_id}")
        user_data["account_id"] = account_id
    else:
        print("No 'account_id' found in the output.")

    # Check if the parsed JSON has "trial_status" and print its value
    trial_status = json_output.get('trial_status')
    if trial_status is not None:
        #print(f"Trial status: {trial_status}")
        user_data["trial_status"] = trial_status
    else:
        print("No 'trial_status' found in the output.")

    # Check if the parsed JSON has "trial_expiration_time" and print its value
    trial_expiration_time = json_output.get('trial_expiration_time')
    if trial_expiration_time is not None:
        #print(f"Trial expiration time: {trial_expiration_time}")
        user_data["trial_expiration_time"] = trial_expiration_time
    else:
        print("No 'trial_expiration_time' found in the output.")

    # Check if the parsed JSON has "trial_billing_group_id" and print its value
    trial_billing_group_id = json_output.get('trial_billing_group_id')
    if trial_billing_group_id is not None:
        #print(f"Trial billing group id: {trial_billing_group_id}")
        user_data["trial_billing_group_id"] = trial_billing_group_id
    else:
        print("No 'trial_billing_group_id' found in the output.")

    # Check if the parsed JSON has "tenant_id" and print its value
    tenant_id = json_output.get('root_account', {}).get('tenant_id', '')
    if tenant_id is not None:
        #print(f"Tenant id: {tenant_id}")
        user_data["tenant_id"] = tenant_id
    else:
        print("No 'tenant_id' found in the output.")

    # Check if the parsed JSON has "primary_billing_group_id" and print its value
    primary_billing_group_id = json_output.get('root_account', {}).get('primary_billing_group_id', '')
    if primary_billing_group_id is not None:
        #print(f"Tenant id: {primary_billing_group_id}")
        user_data["primary_billing_group_id"] = primary_billing_group_id
    else:
        print("No 'primary_billing_group_id' found in the output.")



    # 2. check Organization to get Account_ID
    # aapi billing group describe --billing-group-id 45d80741-2f15-4854-b0ab-344ce7bec933 --json
    print("Checking Billing group with ID " + str(user_data["trial_billing_group_id"]) + "...")
    billing_command = admin_api_alias + ["billing", "group", "describe", "--billing-group-id", str(user_data["trial_billing_group_id"]), "--json"]
    

    output, error = run_command(billing_command)
    if error:
        print("Error from api command:\n", error)
        return
    #else:
    #    print(output)
    
  # Parse the JSON output
    json_output, parse_error = parse_json_output(output)
    if parse_error:
        print(parse_error)
    #else:
    #    print("Parsed JSON Output:\n", json.dumps(json_output, indent=4))

    # Check if the parsed JSON has "credits array"
    credits = json_output.get('credits')
    if credits is not None:
        #print(f"Credits: {credits}")
        user_data["user_credits"] = credits
    else:
        print("No 'credit_code' found in the output.")

    # Check if the parsed JSON has "projects"
    projects = json_output.get('projects')
    if projects is not None:
        #print(f"Projects: {projects}")
        user_data["user_projects"] = projects
    else:
        print("No 'projects' found in the output.")


    # 3. check Billing group to get invoices
    # aapi billing invoice list --billing-group-id 45d80741-2f15-4854-b0ab-344ce7bec933 --json
    print("Checking Invoices for Billing group with ID " + str(user_data["trial_billing_group_id"]) + "...")
    billing_command = admin_api_alias + ["billing", "invoice", "list", "--billing-group-id", str(user_data["trial_billing_group_id"]), "--json"]
    
    output, error = run_command(billing_command)
    if error:
        print("Error from api command:\n", error)
        return
    #else:
    #    print(output)
    
    # Parse the JSON output
    json_output, parse_error = parse_json_output(output)
    if parse_error:
        print(parse_error)
    #else:
    #    print("Parsed JSON Output:\n", json.dumps(json_output, indent=4))

    # Check if the parsed JSON has "credits array"
    invoices = json_output
    if invoices is not None:
        #print(f"Credits: {invoices}")
        user_data["user_invoices"] = invoices
    else:
        print("No 'invoices' found in the output.")


    # 4. Getting trials. Commented out, seems same info as from billing froup
    '''
    for trial in user_data["user_credits"]:
        # aapi credits describe trial-v3c5l6tlu0cjx4 --json
        print("Checking Credits for credit_code with ID " + str(trial["credit_code"]) + "...")
        trial_command = admin_api_alias + ["credits", "describe", str(trial["credit_code"]), "--json"]
    
        output, error = run_command(trial_command)
        if error:
            print("Error from api command:\n", error)
            return
        #else:
        #    print(output)
    
        # Parse the JSON output
        json_output, parse_error = parse_json_output(output)
        if parse_error:
            print(parse_error)
        #else:
        #    print("Parsed JSON Output:\n", json.dumps(json_output, indent=4))

        # Check if the parsed JSON has "credits array"
        credits = json_output
        if invoices is not None:
            #print(f"Credits: {invoices}")
            trial["credit_data"] = credits
        else:
            print("No 'invoices' found in the output.")
    '''
    print(user_data)


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Run user delete pre-check.')
    parser.add_argument('--email', required=True, help='Email of the user')
    parser.add_argument('--org', required=True, help='Organization ID')

    # Parse the arguments
    args = parser.parse_args()
    main(args.email, args.org)

