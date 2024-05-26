import sqlite3
import json


class DataBase:
    def __init__(self, path: str):
        self.path = path
        try:
            self.connection = sqlite3.connect(path, check_same_thread=False)
            self.cursor = self.connection.cursor()
        except sqlite3.Error as error:
            print(f"Ошибка подключения: {error}")
        self.validation_cabinet = [f"it-{i}" for i in range(1, 18)] + ["ГУК Б-320", "ГУК Б-322"]

    def add_from_json(self, path: str):
        with open(path, encoding="utf-8") as f:
            tmp_data = json.load(f)
        for day in tmp_data.keys():
            if day not in ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']:
                continue
            lessons = tmp_data[day]
            for les in lessons["lessons"]:
                if les["cabinet"] in self.validation_cabinet:
                    try:
                        self.cursor.execute(
                            "INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (
                                les["cabinet"],
                                les["group"],
                                " ".join(les["teachers"]),
                                les["time_start"],
                                les["time_end"],
                                les["subject"],
                                lessons["date"],
                                None,
                                1,
                                1,
                            ),
                        )
                    except sqlite3.Error as error:
                        print(f"Ошибка добавление кабинета: {error}")
        self.connection.commit()

    def create_table(self):
        try:
            self.cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='Class'"
            )
            if self.cursor.fetchone() is None:
                self.cursor.execute(
                    'CREATE TABLE "Class" ("Cabinet" TEXT NOT NULL, '
                    '"Group " NUMERIC, "Teacher" TEXT NOT NULL, '
                    '"TimeStart" TEXT NOT NULL, "TimeFinish" TEXT NOT NULL, '
                    '"Name" TEXT NOT NULL, "Date" TEXT NOT NULL, '
                    '"id" TEXT UNIQUE, '
                    '"Regularity" BIT, '
                    '"Type"	BIT)'
                )
                self.connection.commit()
                return True
        except sqlite3.Error as error:
            print(f"Ошибка получения: {error}")
            return False
        return False

    def delete_table(self):
        try:
            self.cursor.execute("DROP table if exists Class")
        except sqlite3.Error as error:
            print(f"Ошибка удаления таблицы: {error}")

    def select_something(self, request: str):
        try:
            self.cursor.execute(f"SELECT {request} FROM Class")
            return self.cursor.fetchall()
        except sqlite3.Error as error:
            print(f"Ошибка выбора: {error}")

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
                    "INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (
                        cabinet,
                        group,
                        teacher,
                        time_start,
                        time_end,
                        name,
                        date,
                        None,
                        regularity,
                        0,
                    ),
                )
                self.connection.commit()
                return True
        except sqlite3.Error as error:
            print(f"Ошибка добавления: {error}")
            return False
        return False

    def delete_lesson(self, cabinet, time_start, date):
        try:
            self.cursor.execute(
                "DELETE FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?",
                (cabinet, time_start, date),
            )
            self.connection.commit()
        except sqlite3.Error as error:
            print(f"Ошибка удаления пары: {error}")

    def is_lesson_in_table(self, cabinet, time_start, date) -> bool:
        try:
            return (
                    len(
                        self.cursor.execute(
                            "SELECT Cabinet, TimeStart, Date FROM Class WHERE Cabinet = ? "
                            "AND TimeStart = ? AND Date = ?",
                            (cabinet, time_start, date),
                        ).fetchall()
                    )
                    > 0
            )
        except sqlite3.Error as error:
            print(f"Ошибка выбора:{error}")

    def get_lesson(self, cabinet, time_start, date):
        try:
            row = self.cursor.execute(
                "SELECT * FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?",
                (cabinet, time_start, date),
            ).fetchall()
            if len(row) > 0:
                return DataBase.__from_tuple_to_dict(row[0])
        except sqlite3.Error as error:
            print(f"Ошибка выбора:{error}")
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
            print(f"Ошибка обновления: {error}")

    def load_lessons_by_dates(self, date_start, date_finish):
        data_from = date_start
        data_to = date_finish
        try:
            db_data = self.cursor.execute(
                f"SELECT * FROM Class WHERE Date <= '{data_to}' AND Date >= '{data_from}'"
            ).fetchall()
        except sqlite3.Error as error:
            print(f"Ошибка подключения: {error}")
            return None
        res = []
        for lesson in db_data:
            res.append(DataBase.__from_tuple_to_dict(lesson))
        return res

    def add_id(self, cabinet, time_start, date, google_id):
        try:
            self.cursor.execute(
                "UPDATE Class SET id = ? WHERE Cabinet = ? AND TimeStart = ? AND Date = ?",
                (google_id, cabinet, time_start, date),
            )
            self.connection.commit()
        except sqlite3.Error as error:
            print(f"Ошибка при ID:{error}")

    def get_id(self, cabinet, time_start, date):
        try:
            return self.cursor.execute(
                "SELECT id FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?",
                (cabinet, time_start, date),
            ).fetchall()[0][0]
        except sqlite3.Error as error:
            print(f"Ошибка при ID: {error}")

    @staticmethod
    def __from_tuple_to_dict(input_tuple: tuple) -> dict:
        return {
            "cabinet": input_tuple[0],
            "group": input_tuple[1],
            "teacher": input_tuple[2],
            "time_start": input_tuple[3],
            "time_finish": input_tuple[4],
            "subject": input_tuple[5],
            "date": input_tuple[6],
            "google_id": input_tuple[7],
            "regularity": input_tuple[8],
            "type": input_tuple[9],
        }

    def __del__(self):
        self.connection.close()
