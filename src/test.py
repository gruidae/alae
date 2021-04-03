import pprint
import sys


import subject_gui_helper

from subject_item import SubjectDayPeriod
from subject_item import SubjectTerm


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
    subjects: list = subject_gui_helper.input_subjects(csvFileName)
    # pprint.pprint(subjects)
    _cui_main(subjects)    
