import sqlite3
import json


class DataBase:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()

    def add_from_json(self, path: str):
        with open(path, encoding="utf-8") as f:
            tmp_data = json.load(f)
        for d in tmp_data:
            lesson = tmp_data[d]
            for les in lesson["lessons"]:
                self.cursor.execute('INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (
                    les["cabinet"], 110, ' '.join(les["teachers"]), les['time_start'], les["time_end"], les["subject"],
                    lesson["date"], 1, 1))
        self.connection.commit()

    # def CreateTable(self):
    #     self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Class'")
    #     if (self.cursor.fetchone() == None):
    #         self.cursor.execute(
    #             'CREATE TABLE "Class" ("Cabinet" TEXT NOT NULL, "Group " NUMERIC, "Teacher"	TEXT NOT NULL,
    #             "TimeStart" TEXT NOT NULL, "TimeFinish" TEXT NOT NULL, "Name" TEXT NOT NULL, "Date" TEXT NOT NULL,
    #             "Regularity" BIT, "Type" BIT)')
    #         self.connection.commit()
    #
    # def DeleteTable(self):
    #     self.cursor.execute('DROP table if exists Class')

    def select_something(self, request: str):
        self.cursor.execute(f"SELECT {request} FROM Class")
        return self.cursor.fetchall()

    def add_lesson(self, cabinet: str, group: int, teacher: str, time_start: str, time_end: str, name: str, date: str,
                   regularity: bool) -> bool:
        if not self.is_lesson_in_table(cabinet, time_start, date):
            self.cursor.execute('INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                                (cabinet, group, teacher, time_start, time_end, name, date, regularity, 0))
            self.connection.commit()
            return True
        return False

    def delete_lesson(self, cabinet, time_start, date):
        self.cursor.execute('DELETE FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?',
                            (cabinet, time_start, date))
        self.connection.commit()

    def is_lesson_in_table(self, cabinet, time_start, date) -> bool:
        for row in self.cursor.execute("SELECT Cabinet, TimeStart, Date FROM Class"):
            if (cabinet, time_start, date) == row:
                return True
        return False

    def get_lesson(self, cabinet, time_start, date):
        for row in self.cursor.execute("SELECT * FROM Class"):
            if cabinet in row and time_start in row and date in row:
                return row
        return None

    def load_lessons_by_week(self, week):
        """
        :param week: неделя в формате ГГ.ММ.ДД-ГГ.ММ.ДД
        """
        data_from = week.split('-')[0]
        data_to = week.split('-')[1]
        db_data = self.cursor.execute(
            f"SELECT * FROM Class WHERE Date <= '{data_to}' AND Date >= '{data_from}'").fetchall()
        res = []
        print(db_data)
        for lesson in db_data:
            res.append({"cabinet": lesson[0],
                        "group": lesson[1],
                        "teacher": lesson[2],
                        "time_start": lesson[3],
                        "time_finish": lesson[4],
                        "subject": lesson[5],
                        "date": lesson[6],
                        "regularity": lesson[7],
                        "type": lesson[8]})
        return res

    def __del__(self):
        self.connection.close()


s = DataBase("LessonsDB.db")
s.add_from_json("8i1cМ8О-110Б-23g2w.json")
print(s.load_lessons_by_week("2024.04.08.-2024.04.14"))
