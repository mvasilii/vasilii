import subprocess
import argparse
import json


def run_command(command):
    """Execute a shell command and return the output."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout, None  # Return output and no error
    except subprocess.CalledProcessError as e:
        return None, e.stderr  # Return no output and error


def parse_json_output(output):
    """Parse the JSON output and return the corresponding Python object."""
    try:
        return json.loads(output), None
    except json.JSONDecodeError as e:
        return None, f"Failed to parse JSON: {e}"


def extract_data(json_output, fields):
    """Extract specified fields from JSON output."""
    extracted_data = {}
    for field in fields:
        value = json_output
        for key in field[:-1]:  # Get nested field values by traversing keys
            value = value.get(key, None)
            if value is None:
                break
        extracted_data[field[-1]] = value if value is not None else None
        
    return extracted_data


def main(email, org):
    admin_api_alias = ["python3", "-m", "aiven.rest.admin.cli", "--api-production", "--json"]
    user_data = {}
    
    # Fetch organization data
    print(f"Checking Account from the Organization '{org}'...")
    account_command = admin_api_alias + ["organization", "describe", str(org), "--json"]

    output, error = run_command(account_command)
    if error:
        print("Error from API command:\n", error)
        return
    
    # Parse the JSON output
    json_output, parse_error = parse_json_output(output)
    if parse_error:
        print(parse_error)
        return

    # Print raw JSON output for debugging
    print("Raw JSON Output from Organization API:")
    print(json.dumps(json_output, indent=4))

    # Define fields to extract
    org_fields = [
        (('root_account', 'account_id'), 'account_id'),
        (('trial_status',), 'trial_status'),
        (('trial_expiration_time',), 'trial_expiration_time'),
        (('trial_billing_group_id',), 'trial_billing_group_id'),
        (('root_account', 'tenant_id'), 'tenant_id'),
        (('root_account', 'primary_billing_group_id'), 'primary_billing_group_id'),
    ]

    # Extract organization data
    user_data.update(extract_data(json_output, org_fields))

    # Output the user_data for checking
    print("User data after extraction:")
    print(json.dumps(user_data, indent=4))

    # Check if trial billing group id is available
    trial_billing_group_id = user_data.get('trial_billing_group_id')
    if trial_billing_group_id:
        print(f"Checking Billing group with ID '{trial_billing_group_id}'...")

        billing_command = admin_api_alias + ["billing", "group", "describe", "--billing-group-id", trial_billing_group_id, "--json"]
        output, error = run_command(billing_command)
        if error:
            print("Error from API command:\n", error)
            return

        billing_json_output, parse_error = parse_json_output(output)
        if parse_error:
            print(parse_error)
            return

        # Print billing JSON output for debugging
        print("Raw JSON Output from Billing Group API:")
        print(json.dumps(billing_json_output, indent=4))

        # Extract billing information
        billing_fields = [
            (('credits',), 'user_credits'),
            (('projects',), 'user_projects'),
        ]
        user_data.update(extract_data(billing_json_output, billing_fields))

        # Print the updated user_data for checking
        print("User data after extraction from billing:")
        print(json.dumps(user_data, indent=4))

        # Now check invoices
        print(f"Checking Invoices for Billing group with ID '{trial_billing_group_id}'...")
        invoice_command = admin_api_alias + ["billing", "invoice", "list", "--billing-group-id", trial_billing_group_id, "--json"]
        
        output, error = run_command(invoice_command)
        if error:
            print("Error from API command:\n", error)
            return
        
        invoices_json_output, parse_error = parse_json_output(output)
        if parse_error:
            print(parse_error)
            return

        # Print invoices JSON output for debugging
        print("Raw JSON Output from Invoices API:")
        print(json.dumps(invoices_json_output, indent=4))

        user_data["user_invoices"] = invoices_json_output if invoices_json_output is not None else []

    # Final output
    print("Final User Data:")
    print(json.dumps(user_data, indent=4))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run user delete pre-check.')
    parser.add_argument('--email', required=True, help='Email of the user')
    parser.add_argument('--org', required=True, help='Organization ID')

    args = parser.parse_args()
    main(args.email, args.org)
