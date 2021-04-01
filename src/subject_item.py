import re

from enum import Enum


_SUBJECT_TERM_SUFFIX = "学期"


class ISTMajor:
    MA  = "情報基礎数学"
    IPS = "情報数理学"
    CS  = "コンピュータサイエンス"
    IS  = "情報システム工学"
    NW  = "情報ネットワーク学"
    MM  = "マルチメディア工学"
    BI  = "バイオ情報工学"
    
    __csvFileDict = {
        MA:  "data/ma.csv",
        IPS: "data/ips.csv",
        CS:  "data/cs.csv",
        IS:  "data/is.csv",
        NW:  "data/nw.csv",
        MM:  "data/mm.csv",
        BI:  "data/bi.csv"   
    }
    
    __majors = [
        MA, IPS, CS, IS, NW, MM, BI
    ]
    
    @staticmethod
    def csvFileDict() -> dict:
        retVal = {}
        for (key, value) in ISTMajor.__csvFileDict.items(): 
            retVal[key] = value
        return retVal
    
    @staticmethod
    def majors() -> list:
        return [major for major in ISTMajor.__majors]


class SubjectTerm(Enum):
    SPRING      = "春"
    SUMMER      = "夏"
    AUTUMN      = "秋"
    WINTER      = "冬"
    WHOLE_YEAR  = "通年"
    INTENSIVE   = "集中"
    MULTI_YEAR  = "年度跨り"
    OTHERS      = "その他"
    
    def __gt__(self, other):
        selfIdx = SubjectTerm.index(self)
        otherIdx = SubjectTerm.index(other)
        return selfIdx > otherIdx
    
    def __hash__(self):
        return hash(self.name)
    
    def __lt__(self, other):
        selfIdx = SubjectTerm.index(self)
        otherIdx = SubjectTerm.index(other)
        return selfIdx < otherIdx
    
    def __str__(self):
        return self.value
    
    @staticmethod
    def toTerms(value: str) -> list:
        tmp = re.sub(_SUBJECT_TERM_SUFFIX+"$", "", value)
        tmp = [tmp0.strip() for tmp0 in tmp.split("～")]
        if tmp[0] == SubjectTerm.WHOLE_YEAR.value:
            return [
                SubjectTerm.SPRING,
                SubjectTerm.SUMMER,
                SubjectTerm.AUTUMN,
                SubjectTerm.WINTER
            ]
        return [SubjectTerm.of(val) for val in tmp]
        
    @staticmethod
    def of(value: str):
        for term in SubjectTerm:
            if term.value == value:
                return term
        errmsg = "\"" + value + "\" is not defined in SubjectTerm."
        raise ValueError(errmsg)
        

class SubjectDay(Enum):
    MONDAY    = "月"
    TUESDAY   = "火"
    WEDNESDAY = "水"
    THURSDAY  = "木"
    FRIDAY    = "金"
    SATURDAY  = "土"
    SUNDAY    = "日"
    OTHERS    = "他"
    
    def __gt__(self, other):
        selfIdx = SubjectDay.index(self)
        otherIdx = SubjectDay.index(other)
        return selfIdx > otherIdx
        
    def __hash__(self):
        return hash(self.name)

    def __lt__(self, other):
        selfIdx = SubjectDay.index(self)
        otherIdx = SubjectDay.index(other)
        return selfIdx < otherIdx
    
    def __str__(self):
        return self.value
        
    @staticmethod
    def of(value: str):
        for day in SubjectDay:
            if day.value == value:
                return day
        errmsg = "\"" + value + "\" is not defined in SubjectDay."
        raise ValueError(errmsg)


class SubjectDayPeriod:
    def __init__(self, day: SubjectDay, period: int):
        self.__day    = day
        self.__period = period
    
    def __eq__(self, other):
        if self is other:
            return True
        elif other is None:
            return False
        elif type(other) is not SubjectDayPeriod:
            return False
        return self.__day == other.__day \
            and self.__period == other.__period
    
    def __gt__(self, other):
        if self.__day > other.__day:
            return True
        elif self.__day < other.__day:
            return False
        else:
            return self.__period > other.__period
    
    def __hash__(self):
            return hash(self.__day) + self.__period        
    
    def __lt__(self, other):
        if self.__day < other.__day:
            return True
        elif self.__day > other.__day:
            return False
        else:
            return self.__period < other.__period       
    
    def __repr__(self):
        return "SubjectDayPeriod(day=" + repr(self.__day) \
            + ",period=" + repr(self.__period) + ")"
    
    def __str__(self):
        return "".join([str(self.__day), str(self.__period)])
    
    @staticmethod
    def toDayPeriods(value: str):
        chars = list(value)
        return [
            SubjectDayPeriod._toDayPeriod([chars[idx], chars[idx+1]]) \
                for idx in range(0, len(chars), 2)
        ]
            
    @staticmethod
    def _toDayPeriod(values: list):
        [day, period] = values
        # 型変換
        day: SubjectDay = SubjectDay.of(day)
        period: int = int(period)
        return SubjectDayPeriod(day, period)