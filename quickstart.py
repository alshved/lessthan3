import os.path
import DB_api

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

 
def Load_Weekly_Schedule(week):
    try:
        # Call the Calendar API
        pair = []
        pairs = DB_api.s.Load_Lessons_By_Week(week)
        for pair in pairs:
            Load_One_Pair(pair)

    except HttpError as error:
        print(f"An error occurred: {error}")

      
def Load_One_Pair(pair):
    try:
      service = build("calendar", "v3", credentials=creds)
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
                  service.events().insert(calendarId="primary", body=new_pair).execute()
              )
      print("Event created: %s" % (event.get("htmlLink")))

    except HttpError as error:
        print(f"An error occurred: {error}")


if __name__ == "__main__":
    creds = None
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
    Load_Weekly_Schedule("2024.02.14-2024.02.16")