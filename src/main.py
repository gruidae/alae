import json
import time
import tkinter

from tkinter import ttk


import subject_gui_helper

from subject_item import ISTMajor
from subject_item import SubjectDay
from subject_item import SubjectDayPeriod
from subject_item import SubjectTerm


class GUIMain:
    __WIDTH_MIN  = 800
    __HEIGHT_MIN = 250
    
    __BORDER_WIDTH   = 3
    __BUTTON_WIDTH   = 10
    __PULLDOWN_WIDTH = 7
    
    __RESULT_MAX = 100
    
    def __init__(self):
        pass
    
    @staticmethod
    def __generateRootWindow(
            title: str,
            width: int,
            height: int
        ):
        root = tkinter.Tk()
        root.title(title)
        root.geometry("x".join([str(width), str(height)]))
        root.minsize(width=width, height=height)
        return root
        
    @staticmethod
    def __generateCombobox(
            parentFrame,
            values: list
        ):
        # comboboxの幅
        maxLen = max([
            len(value) for value in values
        ]) + GUIMain.__PULLDOWN_WIDTH
        # comboboxで指定した値を格納する変数の名前を指定
        # variableName = tkinter.StringVar(refValiable)
        combobox = ttk.Combobox(
            parentFrame,
            # textvariable = variableName,
            values  = values,
            state   = "readonly",
            width   = maxLen,
            height  = len(values)
        )
        return combobox
    
    
    def __searchSubjects(self):
        majorName = self.__majorCombobox.get()
        if majorName is None or len(majorName) < 1:
            self.__finishOutputText.set(
                "専攻を選択してください．"
            )
            return
        fileName  = ISTMajor.csvFileDict()[majorName]
        subjects  = subject_gui_helper.input_subjects(fileName)
        try:
            term = SubjectTerm.of(self.__termCombobox.get())
        except ValueError:
            term = None
            dayPeriod = None
        else:
            try:
                dayPeriod = SubjectDayPeriod(
                    SubjectDay.of(self.__dayCombobox.get()),
                    int(self.__periodCombobox.get())
                )
            except ValueError:
                dayPeriod = None
        
        results = []  # 検索結果
        for subject in subjects:
            if term is None:
                pass
            elif term not in subject.terms:
                continue
            if dayPeriod is None or dayPeriod in subject.dayPeriods:
                results.append(subject)
        if len(results) > self.__RESULT_MAX:
            self.__finishOutputText.set(
                str(self.__RESULT_MAX) + "件を超えました．"
            )
            return
        elif len(results) < 1:
            self.__finishOutputText.set("受講可能な科目が存在しません．")
            return
        # 出力文字列の生成
        jsonText = {
            "専攻": majorName,
            "履修登録期間": str(term),
            "曜日・時限": str(dayPeriod),
            "履修可能科目": [
                subject.toJSON() for subject in results
            ]
        }
        self.__finishOutputText.set(
            "\"tmp/out.json\"に受講可能な科目一覧を保存しました．"
        )
        with open("tmp/out.json", "w", encoding = "utf-8") as fp:
            json.dump(jsonText, fp, indent = 2, ensure_ascii = False)
        time.sleep(1)
        
    def main(self):
        self.__root = self.__generateRootWindow(
            "高度教養教育科目（情報科学研究科）",  # title
            self.__WIDTH_MIN,                  # width
            self.__HEIGHT_MIN                  # height
        )
        
        # トップレベルフレームの設定
        self.__topFrame = ttk.Frame(self.__root, padding=10)
        
        # 検索条件指定フレーム
        self.__searchFrame = ttk.Frame(
            self.__topFrame,
            width       = self.__WIDTH_MIN,
            height      = 200,
            borderwidth = self.__BORDER_WIDTH,
            relief      = "solid",
            padding     = self.__BORDER_WIDTH
        )
        
        # 検索条件指定フレーム
        self.__searchQueryFrame = ttk.Frame(self.__searchFrame)
        
        # 専攻指定
        self.__majorLabel = ttk.Label(
            self.__searchQueryFrame,
            text    = "専攻",
            padding = (5, 10)
        )
        self.__majorCombobox = self.__generateCombobox(
            self.__searchQueryFrame,
            ISTMajor.majors()
        )
        
        # 学期検索
        self.__termLabel = ttk.Label(
            self.__searchQueryFrame,
            text    = "学期",
            padding = (5, 10)
        )
        self.__termCombobox = self.__generateCombobox(
            self.__searchQueryFrame,
            [str(term) for term in SubjectTerm]
        )
        
        # 曜日検索
        self.__dayLabel = ttk.Label(
            self.__searchQueryFrame,
            text    = "曜日",
            padding = (5, 10)
        )
        self.__dayCombobox = self.__generateCombobox(
            self.__searchQueryFrame,
            [str(day) for day in SubjectDay]
        )
        
        # 時限検索
        self.__periodLabel = ttk.Label(
            self.__searchQueryFrame,
            text    = "時限",
            padding = (5, 10)
        )
        self.__periodCombobox = self.__generateCombobox(
            self.__searchQueryFrame,
            [str(i) for i in range(7)]
        )
        
        
        # ボタン
        self.__button = ttk.Button(
            self.__searchFrame,
            text  = "検索",
            width = self.__BUTTON_WIDTH,
            command = self.__searchSubjects
        )
        
        # 検索結果表示
        self.__finishOutputText = tkinter.StringVar()
        self.__finishOutputText.set(
            "「検索」ボタンを押すと\"tmp/out.json\"に受講可能な科目一覧が保存されます．"
        )
        self.__finishOutputLabel = ttk.Label(
            self.__topFrame,
            textvariable = self.__finishOutputText
        )
        
        # レイアウト
        self.__topFrame.pack(side = tkinter.TOP)
        
        self.__majorLabel.pack(side = tkinter.LEFT)
        self.__majorCombobox.pack(side = tkinter.LEFT)
        self.__termLabel.pack(side = tkinter.LEFT)
        self.__termCombobox.pack(side = tkinter.LEFT)
        self.__dayLabel.pack(side = tkinter.LEFT)
        self.__dayCombobox.pack(side = tkinter.LEFT)
        self.__periodLabel.pack(side = tkinter.LEFT)
        self.__periodCombobox.pack(side = tkinter.LEFT)
        self.__searchQueryFrame.pack(side = tkinter.TOP)
        self.__button.pack(side = tkinter.TOP)
        self.__searchFrame.pack(side = tkinter.TOP)
        
        self.__finishOutputLabel.pack(side = tkinter.TOP)
        
        # windowに描画
        self.__root.mainloop()
    
if __name__ == "__main__":
    gui = GUIMain()
    gui.main()
