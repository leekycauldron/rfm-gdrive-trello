#imports can be cleaned up since not all of these are used
import os
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def main():
    #this is authorization stuff copied from the google drive quickstart
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    folder_id = "1Jt8V7b-jpkwRqIX95dJZXr8OYECPJxcH" #this is the id of a test folder I created; will need to be replaced

    service = build("drive", "v3", credentials=creds)

    # the query to search for items in the folder
    query = f"'{folder_id}' in parents"

    while True:
        try:
            # Search for items in the folder
            results = service.files().list(q=query, fields="nextPageToken, files(id, name, createdTime)").execute()

            # Check if any new files since last check
            for file in results.get("files", []):
                created_time = file.get("createdTime")
                file_name = file.get("name")
                file_id = file.get("id")

                #right now this just prints the file to stdout, so this is where it should call trello api
                print(f"New file detected: {file_name} (ID: {file_id}, created at {created_time})")

            # Wait for 10 seconds between checks
            time.sleep(10)

        except HttpError as error:
            print(f"An error occurred: {error}")
            break

if __name__ == "__main__": main()
