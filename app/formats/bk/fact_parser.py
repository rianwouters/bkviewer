from .dates.date import date
from .field import Field, to_int, to_str
from .parsers import Parser
from .events_parser import event_type_map
from models import Fact


class FactParser(Parser):
    grammar = [
        Field('type', 3, to_int),
        Field('space', 1, to_str),
        Field('descr', 150, to_str),
        Field('date1', 20, to_str),
        Field('date2', 20, to_str),
        # 1 = "event started date1 and ended date 2", 2 = "event between date1 and date2", 0 or empty = on date1
        Field('date_type', 1, to_str),
        Field('unused1?', 123, to_str),
        Field('custom_name', 18, to_str),
        Field('unused2?', 30, to_str),
    ]

    def handle(self, r, n, ref):
        name = r['custom_name']
        fact = Fact(name if name else event_type_map[r['type']], date(r), ref, r['descr'])
        ref.events[n-1] = fact
        return fact
