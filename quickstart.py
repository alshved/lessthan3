import os.path
import DBApi

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CALENDARID = 'f25344e2649d967c78566a061a06fae6490a162c9a7b678e61e6171f1fac37c0@group.calendar.google.com'


class GoogleApi:

    def __init__(self):
        self.creds = None
        self.s = DBApi.DataBase("LessonsDB.db")
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists("token.json"):
            self.creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self.flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                self.creds = self.flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.creds.to_json())
        self.service = build("calendar", "v3", credentials=self.creds)

    # Создаём расписание пар в Google calendar на заданный период
    # start - время начала периода в формате ГГГГ.ММ.ДД
    # finish - время окончания периода в формате ГГГГ.ММ.ДД
    def load_weekly_schedule(self, start, finish):
        try:
            pair = []
            pairs = self.s.load_lessons_by_dates(start, finish)
            for pair in pairs:
                self.load_one_pair(pair)

        except HttpError as error:
            print(f"An error occurred: {error}")

    # Создаём одну пару, передаём на вход словарь с информацией о паре
    def load_one_pair(self, pair):
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
                self.service.events().insert(calendarId=CALENDARID, body=new_pair, sendUpdates='all').execute()
            )
            eventId = event.get('id')
            print(eventId)
            self.s.add_id(pair["cabinet"], pair["time_start"], pair["date"], eventId)
            print("Event created: %s" % (event.get("htmlLink")))

        except HttpError as error:
            print(f"An error occurred: {error}")

    # Удаляем все пары из заданного периода 
    # start - время начала периода в формате ГГГГ.ММ.ДД
    # finish - время окончания периода в формате ГГГГ.ММ.ДД
    def delete_weekly_schedule(self, start, finish):
        try:
            pair = []
            pairs = self.s.load_lessons_by_dates(start, finish)
            for pair in pairs:
                self.delete_one_pair(pair)

        except HttpError as error:
            print(f"An error occurred: {error}")

    # Удаляем пару из google календаря, передаём на вход словарь с информацией о паре
    def delete_one_pair(self, pair):
        event_id = self.s.get_id(pair["cabinet"], pair["time_start"], pair["date"])
        event = self.service.events().delete(calendarId=CALENDARID, eventId=event_id).execute()
        print(event)

    # Обновляем информацию о паре, на вход передаются два словаря один с информацией о старой паре второй о новой
    def update_one_pair(self, pair, new_pair):
        self.delete_one_pair(pair)
        self.load_one_pair(new_pair)
