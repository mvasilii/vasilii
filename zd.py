import base64
import requests
import getpass

def authenticate_and_get_data(url, username, password):
    # Making a GET request to the ZenDesk API with Basic Authentication
    response = requests.get(url, auth=(username, password))
    
    if response.status_code == 200:
        print("Successfully authenticated and retrieved data:")
        return response.json()  # Return the JSON response if successful
    else:
        print(f"Failed to authenticate or retrieve data. Status code: {response.status_code}")
        print("Response:", response.text)
        return None
    
def main():
    zendesk_url = "https://aivenhelp.zendesk.com/api/v2/users.json"

    username = "vasilii.mikhailov@aiven.io"
    password = getpass.getpass("Enter your password: ")
    
    #credentials = username + ":" + password
    #encoded_credentials = base64.b64encode(credentials.encode()).decode()
    #print(encoded_credentials)
    data = authenticate_and_get_data(zendesk_url, username, password)
    
    if data is not None:
        # Print or process the data as needed
        print(data)

if __name__ == "__main__":
    main()
