import sqlite3
import json


class data_base:
    def __init__(self, path: str):
        self.path = path
        try:
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as error:
            print("Ошибка подключения")
            return 1
        self.validation_cabinet = [f"it-{i}" for i in range(1, 18)] + ["320", "322"]

    def add_from_json(self, path: str):
        with open(path, encoding="utf-8") as f:
            tmp_data = json.load(f)
        for d in tmp_data:
            lesson = tmp_data[d]
            for les in lesson["lessons"]:
                if les["cabinet"] in self.validation_cabinet:
                    try:
                        self.cursor.execute(
                            "INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                les["cabinet"],
                                110,
                                " ".join(les["teachers"]),
                                les["time_start"],
                                les["time_end"],
                                les["subject"],
                                lesson["date"],
                                None,
                                1,
                                1,
                            ),
                        )
                    except sqlite3.Error as error:
                        print("Ошибка добавление кабинета")
                        return 1
        self.connection.commit()

    def create_table(self):
        try:
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Class'"
            )
            if self.cursor.fetchone() == None:
                self.cursor.execute(
                    'CREATE TABLE "Class" ("Cabinet"	TEXT NOT NULL, "Group "	NUMERIC, "Teacher"	TEXT NOT NULL, "TimeStart"	TEXT NOT NULL, "TimeFinish"	TEXT NOT NULL, "Name" TEXT NOT NULL, "Date" TEXT NOT NULL, "GoogleID" TEXT UNIQUE, "Regularity"	BIT, "Type"	BIT)'
                )
                self.connection.commit()
                return True
        except sqlite3.Error as error:
            print("Ошибка получения")
            return False
        return False

    def delete_table(self):
        try:
            self.cursor.execute("DROP table if exists Class")
        except sqlite3.Error as error:
            print("Ошибка удаления таблицы")
            return 1

    def select_something(self, request: str):
        try:
            self.cursor.execute(f"SELECT {request} FROM Class")
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            print("Ошибка выбора")
            return 1

    def add_lesson(
        self,
        cabinet: str,
        group: int,
        teacher: str,
        time_start: str,
        time_end: str,
        name: str,
        date: str,
        regularity: bool,
    ) -> bool:
        try:
            if (
                not self.is_lesson_in_table(cabinet, time_start, date)
                and cabinet in self.validation_cabinet
            ):
                self.cursor.execute(
                    "INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        cabinet,
                        group,
                        teacher,
                        time_start,
                        time_end,
                        name,
                        date,
                        regularity,
                        0,
                    ),
                )
                self.connection.commit()
                return True
        except sqlite3.Error as error:
            print("Ошибка добавления")
            return False
        return False

    def delete_lesson(self, cabinet, time_start, date) -> bool:
        try:
            self.cursor.execute(
                "DELETE FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?",
                (cabinet, time_start, date),
            )
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка удаления пары")
            return 1

    def is_lesson_in_table(self, cabinet, time_start, date) -> bool:
        try:
            return (
                len(
                    self.cursor.execute(
                        "SELECT Cabinet, TimeStart, Date FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?",
                        (cabinet, time_start, date),
                    ).fetchall()
                )
                > 0
            )
        except sqlite3.Error as error:
            print("Ошибка выбора")
            return None

    def get_lesson(self, cabinet, time_start, date):
        try:
            row = self.cursor.execute(
                "SELECT * FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?",
                (cabinet, time_start, date),
            ).fetchall()
            if len(row) > 0:
                return data_base.__from_tuple_to_dict(row[0])
        except sqlite3.Error as error:
            print("Ошибка выбора")
            return None
        return None

    def update_db_lesson(self, cabinet, time_start, date, newtime_start, new_date):
        try:
            self.cursor.execute(
                "UPDATE Class SET TimeStart = ? AND Date = ? WHERE Cabinet = ? AND TimeStart = ? AND Date = ?",
                (newtime_start, new_date, cabinet, time_start, date),
            )
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка обновления")
            return 1

    def load_lessons_by_dates(self, date_start, date_finish):
        data_from = date_start
        data_to = date_finish
        try:
            db_data = self.cursor.execute(
                f"SELECT * FROM Class WHERE Date <= '{data_to}' AND Date >= '{data_from}'"
            ).fetchall()
        except sqlite3.Error as error:
            print("Ошибка подключения")
            return None
        res = []
        for lesson in db_data:
            res.append(data_base.__from_tuple_to_dict(lesson))
        return res

    def add_id(self, cabinet, time_start, date, ID):
        try:
            self.cursor.execute(
                "UPDATE Class SET GoogleID = ? WHERE Cabinet = ? AND TimeStart = ? AND Date = ?",
                (ID, cabinet, time_start, date),
            )
            self.connection.commit()
        except sqlite3.Error as error:
            print("Ошибка при ID")

    def get_id(self, cabinet, time_start, date, ID):
        try:
            return self.cursor.execute(
                "SELECT GoogleID FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?",
                (cabinet, time_start, date),
            ).fetchall()[0][0]
        except sqlite3.Error as error:
            print("Ошибка при ID")

    def __from_tuple_to_dict(tuple: tuple) -> dict:
        return {
            "cabinet": tuple[0],
            "group": tuple[1],
            "teacher": tuple[2],
            "time_start": tuple[3],
            "time_finish": tuple[4],
            "subject": tuple[5],
            "date": tuple[6],
            "regularity": tuple[7],
            "type": tuple[8],
        }

    def __del__(self):
        self.connection.close()
