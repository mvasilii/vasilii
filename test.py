import apiUtils

def main():
    # API token title in 1password
    note_title = "AVN client token"
    token = apiUtils.get_token(note_title)
    if token:
        print("Token retrieved")
        #print(token)
    else:
        print("Failed to retrieve the secure note.")


if __name__ == "__main__":
    main()