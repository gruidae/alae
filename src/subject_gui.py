import tkinter

from tkinter import ttk


from subject_item import SubjectDay
from subject_item import SubjectDayPeriod
from subject_item import SubjectTerm


_WIDTH_MIN  = 400
_HEIGHT_MIN = 300

"""
_queryTerm   = str(SubjectTerm.SPRING)
_queryDay    = str(SubjectDay.WEDNESDAY)
_queryPeriod = str(0)
"""

def generate_root_window(title: str, width: int, height: int):
    root = tkinter.Tk()
    root.title(title)
    root.geometry("x".join([str(width), str(height)]))
    root.minsize(width=width, height=height)
    return root


def generate_combobox(
        parentFrame,
        values: list
    ):
    # comboboxの幅
    maxLen = max([len(value) for value in values]) + 4
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
    combobox.current(0)
    return combobox
    

def gui_main(subjects: list = []):
    rootWindow = generate_root_window(
        "高度教養教育科目（情報科学研究科）",  # title
        _WIDTH_MIN,                        # width
        _HEIGHT_MIN                        # height
    )
    
    # トップレベルフレームの設定
    topFrame = ttk.Frame(rootWindow, padding=10)
    
    # 検索条件指定フレーム
    searchFrame = ttk.Frame(
        topFrame,
        width       = _WIDTH_MIN,
        height      = 200,
        borderwidth = 10,
        relief      = "solid",
        padding     = 10
    )
    
    # 検索条件指定フレーム
    searchQueryFrame = ttk.Frame(searchFrame)
    
    # 学期検索
    termLabel = ttk.Label(
        searchQueryFrame,
        text    = "学期",
        padding = (5, 10)
    )
    termCombobox = generate_combobox(
        searchQueryFrame,
        [str(term) for term in SubjectTerm]
    )
    
    # 曜日検索
    dayLabel = ttk.Label(
        searchQueryFrame,
        text    = "曜日",
        padding = (5, 10)
    )
    dayCombobox = generate_combobox(
        searchQueryFrame,
        [str(day) for day in SubjectDay]
    )
    
    # 時限検索
    periodLabel = ttk.Label(
        searchQueryFrame,
        text    = "時限",
        padding = (5, 10)
    )
    periodCombobox = generate_combobox(
        searchQueryFrame,
        [str(i) for i in range(1, 7)]
    )
    
    
    # ボタン
    button = ttk.Button(
        searchFrame,
        text = "検索",
        width= 10
    )
    
    
    # 検索結果表示フレーム
    resultFrame = ttk.Frame(
        topFrame,
        width       = _WIDTH_MIN,
        height      = 300,
        borderwidth = 10,
        relief      = "sunken",
        padding     = 10
    )
    
    # レイアウト
    topFrame.pack(side = tkinter.TOP)
    
    termLabel.pack(side = tkinter.LEFT)
    termCombobox.pack(side = tkinter.LEFT)
    dayLabel.pack(side = tkinter.LEFT)
    dayCombobox.pack(side = tkinter.LEFT)
    periodLabel.pack(side = tkinter.LEFT)
    periodCombobox.pack(side = tkinter.LEFT)
    searchQueryFrame.pack(side = tkinter.TOP)
    button.pack(side = tkinter.TOP)
    searchFrame.pack(side = tkinter.TOP)
    
    resultFrame.pack(side = tkinter.TOP)
    
    # windowに描画
    rootWindow.mainloop()

if __name__ == "__main__":
    gui_main()
