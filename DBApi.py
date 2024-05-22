import sqlite3
import json

class DataBase:
  def __init__(self, path: str):
    self.path = path
    self.connection = sqlite3.connect(path)
    self.cursor = self.connection.cursor()
    self.validationCabinet = [f"it-{i}" for i in range(1, 18)] + ["320", "322"]
  
  def AddFromJson(self, path: str):
    with open(path, encoding="utf-8") as f:
      tmpData = json.load(f)
    for d in tmpData:
      lesson = tmpData[d]
      for les in lesson["lessons"]:
        if (les["cabinet"] in self.validationCabinet):
          self.cursor.execute('INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (les["cabinet"], 110, ' '.join(les["teachers"]), les['time_start'], les["time_end"], les["subject"], lesson["date"], 1, 1))
    self.connection.commit()

  def CreateTable(self):
    self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Class'")
    if(self.cursor.fetchone() == None):
      self.cursor.execute('CREATE TABLE "Class" ("Cabinet"	TEXT NOT NULL, "Group "	NUMERIC, "Teacher"	TEXT NOT NULL, "TimeStart"	TEXT NOT NULL, "TimeFinish"	TEXT NOT NULL, "Name"	TEXT NOT NULL, "Date"	TEXT NOT NULL, "Regularity"	BIT, "Type"	BIT)')
      self.connection.commit()
      return True
    return False
   
  def DeleteTable(self):
    self.cursor.execute('DROP table if exists Class')

  def selectSomething(self, request: str):
    self.cursor.execute(f"SELECT {request} FROM Class")
    return self.cursor.fetchall()

  def AddLesson(self, cabinet: str, group: int, teacher: str, timeStart: str, timeEnd: str, name: str, date: str, regularity: bool) -> bool:
    if (not self.IsLessonInTable(cabinet, timeStart, date) and cabinet in self.validationCabinet):
      self.cursor.execute('INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (cabinet, group, teacher, timeStart, timeEnd, name, date, regularity, 0))
      self.connection.commit()
      return True
    return False

  def DeleteLesson(self, cabinet, timeStart, date) -> bool:
    self.cursor.execute('DELETE FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?', (cabinet, timeStart, date))
    self.connection.commit()
  def IsLessonInTable(self, cabinet, timeStart, date) -> bool:
    return (len(self.cursor.execute("SELECT Cabinet, TimeStart, Date FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?", (cabinet, timeStart, date)).fetchall()) > 0)
  
  def GetLesson(self, cabinet, timeStart, date):
    row = self.cursor.execute("SELECT * FROM Class WHERE Cabinet = ? AND TimeStart = ? AND Date = ?", (cabinet, timeStart, date)).fetchall()
    if len(row) > 0:
      return DataBase.__FromTupleToDict(row[0])
    return None
  
  def UpdateDBLesson(self, cabinet, timeStart, date, newtimeStart, newDate):
    self.cursor.execute("UPDATE Class SET TimeStart = ? AND Date = ? WHERE Cabinet = ? AND TimeStart = ? AND Date = ?", (newtimeStart, newDate, cabinet, timeStart, date))
    self.connection.commit()
  
  def loadLessonsByDates(self, dateStart, dateFinish):
        """
        :param week: неделя в формате ГГ.ММ.ДД-ГГ.ММ.ДД
        """
        dataFrom = dateStart
        dataTo = dateFinish
        dbData = self.cursor.execute(
            f"SELECT * FROM Class WHERE Date <= '{dataTo}' AND Date >= '{dataFrom}'").fetchall()
        res = []
        print(dbData)
        for lesson in dbData:
            res.append(DataBase.__FromTupleToDict(lesson))
        return res

  def __FromTupleToDict(tuple: tuple) -> dict:
    return {"Cabinet": tuple[0],
            "Group": tuple[1],
            "Teacher": tuple[2],
            "TimeStart": tuple[3],
            "TimeFinish": tuple[4],
            "Subject": tuple[5],
            "Date": tuple[6],
            "Regularity": tuple[7],
            "Type": tuple[8]}
  
  def __del__(self):
    self.connection.close()