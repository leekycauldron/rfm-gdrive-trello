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
import trelloCreate
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
# the first array is the names of the people, the second array is the folder id for each person
folders = [
        ["Andrew","Bryson", "Daniel", "David", "Nelson", "Rachel", "Ronny", "Sean", "Shalott", "Tamir","Ted"],
        ["1zwyjtLaUkWRacN-gdxElDo05_51uFW39","1eFm2YnjMVWPYtUyEhbajBjC1-YloI2Vc","","1guIi7sZOaUMNRCvnB5bAmDqnxCQCPg7z","1PF4bmd1qW0pbKUIaAIXr58DvS27neLb7","","1C5XOYEKgUu0x_3CX5QpOMKIsQySUJuaI","","1ICoP3zL_mIkfmmr_2V0NoywsMgPOeItA","",""]
        ]

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
    


    service = build("drive", "v3", credentials=creds)

    
    for i in range(len(folders[0])):
        # the query to search for items in the folder
        query = f"'{folders[1][i]}' in parents"
        try:
            # Search for items in the folder
            results = service.files().list(q=query, fields="nextPageToken, files(id, name, createdTime)").execute()

            # Check if any new files since last check
            for file in results.get("files", []):
                created_time = file.get("createdTime")
                file_name = file.get("name")
                file_id = file.get("id")

                #if the file was created today, print it
                if datetime.strptime(created_time, '%Y-%m-%dT%H:%M:%S.%fZ').date() == datetime.today().date():
                    trelloCreate.createCard("https://drive.google.com/file/d/"+file_id, folders[0][i])
                    print(f"New file found: {file_name} (ID: {file_id}, created at {created_time})")
                else:
                    print(f"File found: {file_name} (ID: {file_id}, created at {created_time})")
                

            # Wait for 10 seconds between checks
            time.sleep(10)

        except HttpError as error:
            print(f"An error occurred: {error}")
            break
    print("Done")
    return "OK"

if __name__ == "__main__": main()



#TODO:
# *DONE*  ----- remove the while loop and create two arrays (the arrays will contain name and folder id for each person), loops through it
# *DONE*  ----- time check to see if it was uploaded today
# get folder id from everyone (get folder link from everyone)
#associate folder id with name


#example of files in "for file in results.get("files", []):"
{'id': '1ZTuKrtJe13WBWfQ-0gABqZj68HbZ6VqZmHL9dnfbbUw', 'name': '6', 'createdTime': '2023-02-01T23:50:21.457Z'}
{'id': '1Pf05VB1Oq--63d0O8NfEUn7x4g4awZzO', 'name': 'Sean Huang RPT outline.pdf', 'createdTime': '2023-04-26T18:24:32.891Z'}
