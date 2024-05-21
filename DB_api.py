import sqlite3
import json


class DataBase:
    def __init__(self, path: str):
        self.path = path
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def AddFromJson(self, path: str):
        with open(path, encoding="utf-8") as f:
            tmpData = json.load(f)
        for d in tmpData:
            lesson = tmpData[d]
            for les in lesson["lessons"]:
                self.cursor.execute('INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                les["cabinet"], 110, ' '.join(les["teachers"]), les['time_start'], les["time_end"], les["subject"],
                lesson["date"], 1, 1))
        self.connection.commit()

    def CreateTable(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Class'")
        if (self.cursor.fetchone() == None):
            self.cursor.execute(
                'CREATE TABLE "Class" ("Cabinet"	TEXT NOT NULL, "Group "	NUMERIC, "Teacher"	TEXT NOT NULL, "TimeStart"	TEXT NOT NULL, "TimeFinish"	TEXT NOT NULL, "Name"	TEXT NOT NULL, "Date"	TEXT NOT NULL, "Regularity"	BIT, "Type"	BIT)')
            self.connection.commit()

    def DeleteTable(self):
        self.cursor.execute('DROP table if exists Class')

    def selectSomething(self, request: str):
        self.cursor.execute(f"SELECT {request} FROM Class")
        return self.cursor.fetchall()

    def AddLesson(self, cabinet: str, group: int, teacher: str, timeStart: str, timeEnd: str, name: str, date: str,
                  regularity: bool) -> bool:
        if (not self.IsLessonInTable(cabinet, timeStart, date)):
            self.cursor.execute('INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                (cabinet, group, teacher, timeStart, timeEnd, name, date, regularity, 0))
            self.connection.commit()
            return True
        return False

    def DeleteLesson(self, cabinet, timeStart, date) -> bool:
        self.cursor.execute('DELETE FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?',
                            (cabinet, timeStart, date))
        self.connection.commit()

    def IsLessonInTable(self, cabinet, timeStart, date) -> bool:
        for row in self.cursor.execute("SELECT Cabinet, TimeStart, Date FROM Class"):
            if ((cabinet, timeStart, date) == row):
                return True
        return False

    def GetLesson(self, cabinet, timeStart, date):
        for row in self.cursor.execute("SELECT * FROM Class"):
            if (cabinet in row and timeStart in row and date in row):
                return row
        return None

    def __del__(self):
        self.connection.close()