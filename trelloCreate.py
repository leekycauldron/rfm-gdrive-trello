import requests
import datetime
from creds import *


def createCard(link=None,name=None):
    url = "https://api.trello.com/1/cards"
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    body = {
        "key":KEY,
        "token":TOKEN,
        "idList":"64492238696b4da266e1c10e",
        "name":"New Video",
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

