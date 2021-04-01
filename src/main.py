#!/bin/python3


import csv
import pprint
import sys
# import tkinter

# from tkinter import ttk


from subject import Subject
from subject_item import SubjectDayPeriod
from subject_item import SubjectTerm
# import subject_gui


def _input_subjects(csvFileName: str) -> list:
    # subjects = []  
    rows = None
    with open(csvFileName, encoding="utf-8") as fp:
        rows = [row for row in csv.reader(fp)]
    # Debug
    # for row in rows:
    #     print(row, file=sys.stderr)
    return Subject.toSubjects(rows)


def _cui_main(subjects: list):
    query: str = input("input 学期: ")
    while len(query) > 0:
        term: SubjectTerm = SubjectTerm.of(query)
        day: str = input("input 曜日: ")
        if len(day) < 1:
            break
        
        try:
            period: int = int(input("input 時限: "))
        except ValueError:
            break
        dayPeriod: SubjectDayPeriod = SubjectDayPeriod(day, period)
        
        for subject in subjects:
            if term not in subject.terms:
                result:str = "\n".join([
                    subject.name,
                    subject.graduateSchool,
                    str(subject.credit),
                    str(subject.capacity)
                ])
                print(result+"\n")
                continue
            if dayPeriod in subject.dayPeriods:
                result:str = "\n".join([
                    subject.name,
                    subject.graduateSchool,
                    subject.credit,
                    str(subject.capacity)
                ])
                print(result+"\n")
        
        query = input("input 学期: ")


if __name__ == "__main__":
    csvFileName: str = sys.argv[1]
    subjects: list = _input_subjects(csvFileName)
    # pprint.pprint(subjects)
    _cui_main(subjects)    