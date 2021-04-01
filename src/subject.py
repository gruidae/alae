from subject_item import SubjectDayPeriod
from subject_item import SubjectTerm


class Subject:
    def __init__(
            self,
            name: str,                     # 科目名
            terms: list,                   # 開講期間
            dayPeriods: SubjectDayPeriod,  # 曜日・時限
            credit,                        # 単位数
            graduateSchool: str,           # 開講部局名
            canTakeLectureInM1: bool,      # M1で履修可能か
            canTakeLectureInM2: bool,      # M2で履修可能か
            capacity                       # 収容制限
        ):
        self.__name               = name
        self.__terms              = terms
        self.__dayPeriods         = dayPeriods
        self.__credit             = credit
        self.__graduateSchool     = graduateSchool
        self.__canTakeLectureInM1 = canTakeLectureInM1
        self.__canTakeLectureInM2 = canTakeLectureInM2
        self.__capacity           = capacity
    
    @property
    def capacity(self):
        return self.__capacity
    
    @property
    def credit(self):
        return self.__credit
    
    @property
    def dayPeriods(self):
        return [dayPeriod for dayPeriod in self.__dayPeriods]
    
    @property
    def graduateSchool(self):
        return self.__graduateSchool
    
    @property
    def name(self):
        return self.__name
    
    @property
    def terms(self):
        return [term for term in self.__terms]
    
    def __dict__(self):
        return {
            "name":  self.name,
            "terms": self.terms,
            "dayPeriods": self.dayPeriods,
            "credit": self.credit,
            "graduateSchool": self.graduateSchool,
            "canTakeLectureInM1": self.__canTakeLectureInM1,
            "canTakeLectureInM2": self.__canTakeLectureInM2,
            "capacity": self.capacity
        }
    
    def __eq__(self, other):
        if self is other:
            return True
        elif other is None:
            return False
        elif type(other) is not Subject:
            return False
        elif self.__name != other.__name:
            return False
        else:
            return True
    
    def __hash__(self): 
        return self.__name
    
    def __repr__(self):
        retVal: str = "Subject(name=\"" + self.__name \
            + "\",terms=" + repr(self.__terms) \
            + "\",dayPeriods=" + repr(self.__dayPeriods) \
            + ",credit=" + repr(self.__credit) \
            + ",graduateSchool=\""  + self.__graduateSchool \
            + "\",canTakeLectureInM1=" + repr(self.__canTakeLectureInM1) \
            + ",canTakeLectureInM2=" + repr(self.__canTakeLectureInM2)
        
        if type(self.__capacity) is int:
            retVal += ",capacity=" + repr(self.__capacity) + ")"
        else:
            # 受け入れ人数に制限がない or 独自で定められている場合
            retVal += ",capacity=\"" + self.__capacity + "\")"
        return retVal
    
    def __str__(self):
        return self.__name
    
    def toJSON(self) -> dict:
        return {
            "開講科目名":  self.name,
            "開講期間": [str(term) for term in self.terms],
            "曜日・時限": [str(dayPeriod) for dayPeriod in self.dayPeriods],
            "単位数": self.credit,
            "開講部局": self.graduateSchool,
            "定員": self.capacity
        }
    
    @staticmethod
    def toSubjects(values: list) -> list:
        return [Subject._toSubject(vals) for vals in values]
    
    @staticmethod
    def _toSubject(values: list):
        [
            graduateSchool,      # 開講部局名
            _,                   # 時間割コード（不要）
            name,                # 科目名
            credit,              # 単位数
            canTakeLectureInM1,  # M1で履修可能か
            canTakeLectureInM2,  # M2で履修可能か
            terms,               # 開講期間
            dayPeriods,          # 曜日・時限
            capacity,            # 収容制限
            _,                   # ナンバリングコード（不要）
            _                    # 科目コード（不要）
        ] = values
        
        # 型変換
        terms: list = SubjectTerm.toTerms(terms)
        dayPeriods: list = SubjectDayPeriod.toDayPeriods(dayPeriods)
        canTakeLectureInM1: bool = (canTakeLectureInM1 == "○")
        canTakeLectureInM2: bool = (canTakeLectureInM2 == "○")
        try:
            credit: int = int(credit)
        except ValueError:
            # 単位数が整数でない場合
            credit: float = float(credit)
        try:
            capacity: int = int(capacity)
        except ValueError:
            # 受講可能人数に制限が無い or 別途定められている場合．
            # プログラム上では文字列型として処理するため，型を変化させない
            pass
        
        return Subject(
            name,
            terms,
            dayPeriods,
            credit,
            graduateSchool,
            canTakeLectureInM1,
            canTakeLectureInM2,
            capacity
        )