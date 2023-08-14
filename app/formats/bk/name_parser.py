from .dates.date import date
from .field import Field, to_int, to_str
from .parsers import Parser
from models import Name, NameType


name_type_map = dict([
    (1, NameType.ALSO_KNOWN_AS),
    (5, NameType.NICK),
    (10, NameType.SHORT),
    (15, NameType.ADOPTED),
    (20, NameType.HEBREW),
    (25, NameType.CENSUS),
    (30, NameType.MARIIED),
    (35, NameType.GERMAN),
    (40, NameType.FARM),
    (45, NameType.BIRTH),
    (50, NameType.INDIAN),
    (55, NameType.FORMAL),
    (60, NameType.CURRENT),
    (65, NameType.SOLDIER),
    (68, NameType.FORMERLY_KNOWN_AS),
    (70, NameType.RELIGIOUS),
    (80, NameType.CALLED),
    (85, NameType.INDIGENOUS),
    (88, NameType.TOMBSTONE),
    (95, NameType.OTHER),
])


class NameParser(Parser):
    grammar = [
        Field('type', 3, to_int),
        Field('space', 1, to_str),
        Field('text', 150, to_str),
        Field('date1', 20, to_str),
        Field('date2', 20, to_str),
        # 1 = "event started date1 and ended date 2", 2 = "event between date1 and date2", 0 or empty = on date1
        Field('date_type', 1, to_str),
        Field('unused1?', 11, to_str),
        Field('print_where', 3, to_int),
        Field('unused2?', 157, to_str),
    ]

    def handle(self, r, n, ref):
        name = Name(name_type_map[r['type']], r['text'], date(r))
        ref.names[n] = name
        return name
