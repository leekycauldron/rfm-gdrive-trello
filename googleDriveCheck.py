import os
import time
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
import requests
from creds import *

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
# the first array is the names of the people, the second array is the folder id for each person
folders = [
        ["Andrew","Bryson", "Daniel", "David", "Nelson", "Rachel", "Ronny", "Sean", "Shalott", "Tamir","Ted"],
        ["1zwyjtLaUkWRacN-gdxElDo05_51uFW39","1eFm2YnjMVWPYtUyEhbajBjC1-YloI2Vc","1EWYuzbLHvU8-wN3Nc7ncyvg9h1mjaaJC","1guIi7sZOaUMNRCvnB5bAmDqnxCQCPg7z","1PF4bmd1qW0pbKUIaAIXr58DvS27neLb7","1yf6IJK1YFVCN_BoW1ubK0BSdHfb_Vzxf","1C5XOYEKgUu0x_3CX5QpOMKIsQySUJuaI","1MEcU11EZs0YELzW2Kyd3bG30Lv63lv74","1ICoP3zL_mIkfmmr_2V0NoywsMgPOeItA","1nFMC-zVN58ljN546_i2x-OBxbHebDW7E","18-rwwoOtvAX4OYrwWR9zNrrIWmQnBCyf"]
        ]

def createCard(link=None,name=None,fileName=None):
    url = "https://api.trello.com/1/cards"
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    body = {
        "key":KEY,
        "token":TOKEN,
        "idList":"64492238696b4da266e1c10e",
        "name":"Reflection Video: "+("No file name" if not fileName else fileName),
        "desc":f"""
        
    Link: {link}
    Date Uploaded: {date}
    Name: {name}""",
    }

    response = requests.request("POST",url,params=body)

    data = response.json()
    id = data['id']

    ###### ADD CHECKLIST TO CARD ######
    url = f"https://api.trello.com/1/cards/{id}/checklists"

    body = {
        "key": body["key"],
        "token": body["token"],
        "name": "Tasks",
    }

    response = requests.request("POST",url,params=body)


    ##### Create checklist items #####
    data = response.json()
    id = data['id']

    url = f"https://api.trello.com/1/checklists/{id}/checkItems"

    tasks = ["Edit the video","Add Intro","Add Outro","Add Special Effects","Upload to Social Media"]
    for i in range(len(tasks)):
        body = {
            "key": body["key"],
            "token": body["token"],
            "name": tasks[i],
            "pos": "bottom"
        }

        response = requests.request("POST",url,params=body)

        print(response.status_code)


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
                    createCard("https://drive.google.com/file/d/"+file_id, folders[0][i], file_name)
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