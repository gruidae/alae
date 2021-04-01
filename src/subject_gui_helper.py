import csv


from subject import Subject


def input_subjects(csvFileName: str) -> list:
    # subjects = []  
    rows = None
    with open(csvFileName, encoding="utf-8") as fp:
        rows = [row for row in csv.reader(fp)]
    return Subject.toSubjects(rows)