{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 41,
   "metadata": {},
   "outputs": [],
   "source": [
    "import sqlite3\n",
    "import json\n",
    "\n",
    "class DataBase:\n",
    "  def __init__(self, path: str):\n",
    "    self.path = path\n",
    "    self.connection = sqlite3.connect(path)\n",
    "    self.cursor = self.connection.cursor()\n",
    "  \n",
    "  def AddFromJson(self, path: str):\n",
    "    with open(path, encoding=\"utf-8\") as f:\n",
    "      tmpData = json.load(f)\n",
    "    for d in tmpData:\n",
    "      lesson = tmpData[d]\n",
    "      for les in lesson[\"lessons\"]:\n",
    "        self.cursor.execute('INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (les[\"cabinet\"], 110, ' '.join(les[\"teachers\"]), les['time_start'], les[\"time_end\"], les[\"subject\"], lesson[\"date\"], 0, 1))\n",
    "    self.connection.commit()\n",
    "\n",
    "  def CreateTable(self):\n",
    "    self.cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table' AND name='Class'\")\n",
    "    if(self.cursor.fetchone() == None):\n",
    "      self.cursor.execute('CREATE TABLE \"Class\" (\"Cabinet\"\tTEXT NOT NULL, \"Group \"\tNUMERIC, \"Teacher\"\tTEXT NOT NULL, \"TimeStart\"\tTEXT NOT NULL, \"TimeFinish\"\tTEXT NOT NULL, \"Name\"\tTEXT NOT NULL, \"Date\"\tTEXT NOT NULL, \"Regularity\"\tBIT, \"Type\"\tBIT)')\n",
    "      self.connection.commit()\n",
    "  \n",
    "  def DeleteTable(self):\n",
    "    self.cursor.execute('DROP table if exists Class')\n",
    "\n",
    "  def AddLesson(self, cabinet: str, group: int, teacher: str, timeStart: str, timeEnd: str, name: str, date: str, regularity: bool, type: bool):\n",
    "    self.cursor.execute('INSERT INTO Class VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (cabinet, group, teacher, timeStart, timeEnd, name, date, regularity, type))\n",
    "    self.connection.commit()\n",
    "\n",
    "  def __del__(self):\n",
    "    self.connection.close()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": [
    "a = DataBase(\"LessonsDB.db\")\n",
    "a.DeleteTable()\n",
    "a.CreateTable()\n",
    "a.AddFromJson(\"Data.json\")\n",
    "a.AddLesson(\"1312\", 12, \"Пельмень\", \"12:11\", \"'123:13\", \"Пельменоведение\", \"01.314.13\", 1, 1)"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.9"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
