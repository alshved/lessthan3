import os.path
import DBApi

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDARID = 'f25344e2649d967c78566a061a06fae6490a162c9a7b678e61e6171f1fac37c0@group.calendar.google.com'

 
def load_weekly_schedule(start, finish):
    try:
        # Call the Calendar API
        pair = []
        pairs = s.load_lessons_by_dates(start, finish)
        for pair in pairs:
            load_one_pair(pair)

    except HttpError as error:
        print(f"An error occurred: {error}")

      
def load_one_pair(pair):
    try:
        new_pair = {
                "summary": pair["subject"],
                "location": pair["cabinet"],
                "start": {
                    "dateTime": pair["date"].replace(".", "-")
                    + "T"
                    + pair["time_start"]
                    + ":00+03:00"
                },
                "end": {
                    "dateTime": pair["date"].replace(".", "-")
                    + "T"
                    + pair["time_finish"]
                    + ":00+03:00"
                }
              }
        if (pair['teacher']):
            new_pair['description'] = 'Преподаватель - ' + pair['teacher'] + ', группа - ' + str(pair['group'])
        event = (
                service.events().insert(calendarId=CALENDARID, body=new_pair).execute()
            )
        eventId = event.get('id')
        s.add_id(pair["cabinet"], pair["time_start"], pair["date"], eventId)
        print("Event created: %s" % (event.get("htmlLink")))

    except HttpError as error:
        print(f"An error occurred: {error}")


def delete_one_pair(pair):
    id = s.get_id(pair["cabinet"], pair["time_start"], pair["date"])
    event = service.events().delete(calendarId=CALENDARID, eventId=id).execute()
    print(event)

def update_one_pair(pair, new_pair):
    delete_one_pair(pair)
    load_one_pair(new_pair)


if __name__ == "__main__":
    creds = None
    s = DBApi.data_base("LessonsDB.db")
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("calendar", "v3", credentials=creds)
    load_weekly_schedule("2024.02.14", "2024.02.16")