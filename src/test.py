import csv
import pprint
import sys


import subject_gui_helper

from subject_item import SubjectDay
from subject_item import SubjectDayPeriod
from subject_item import SubjectTerm


def _cui_main(subjects: list):
    query: str = input("input 学期: ")
    while len(query) > 0:
        term: SubjectTerm = SubjectTerm.of(query)
        day: str = input("input 曜日: ")
        if len(day) < 1:
            break
        day: SubjectDay = SubjectDay.of(day)
        try:
            period: int = int(input("input 時限: "))
        except ValueError:
            break
        dayPeriod: SubjectDayPeriod = SubjectDayPeriod(day, period)
        for subject in subjects:
            if term not in subject.terms:
                continue
            if dayPeriod in subject.dayPeriods:
                result:str = "\n".join([
                    subject.name,
                    "  - " + " ".join([str(term) for term in subject.terms]),
                    "  - " + " ".join([str(dp) for dp in subject.dayPeriods]),
                    "  - " + subject.graduateSchool,
                    "  - " + str(subject.credit),
                    "  - " + str(subject.capacity)
                ])
                print(result)
        query = input("input 学期: ")


def _toCSV(subjects: list):
    results = []
    term: SubjectTerm = SubjectTerm.of("秋")
    for day in SubjectDay:
        for period in range(0, 7):
            dayPeriod: SubjectDayPeriod = SubjectDayPeriod(day, period)
            for subject in subjects:
                if subject in results:
                    continue
                if term not in subject.terms:
                    continue
                if dayPeriod in subject.dayPeriods:
                    results.append(subject)
    
    outSubjects:list = [
        [
            subject.name,
            subject.graduateSchool,
            "".join([str(term) for term in subject.terms]),
            "".join([str(dayPeriod) for dayPeriod in subject.dayPeriods]),
            subject.credit,
            subject.capacity
        ] for subject in results
    ]
    outSubjects.insert(0, ["講義名",  "開講部局","開講期間", "曜日時限", "単位数", "制限人数"])
    with open("tmp/autumn.csv", "w", encoding="utf-8") as fp:
        writer = csv.writer(fp)
        writer.writerows(outSubjects)

    

if __name__ == "__main__":
    csvFileName: str = sys.argv[1]
    subjects: list = subject_gui_helper.input_subjects(csvFileName)
    # debug
    # pprint.pprint(subjects)
    # _cui_main(subjects)
    _toCSV(subjects)
