
from .dates.date import date
from .field import Field, to_int, to_str
from .parsers import Parser
from models import Todo, TodoStatus, TodoType


todo_type_map = dict([
    (1, TodoType.RESEARCH),
    (2, TodoType.CORRESPONDENCE),
    (9, TodoType.OTHER),
])

todo_status_map = dict([
    (1, TodoStatus.PLAN),
    (2, TodoStatus.STARTED),
    (9, TodoStatus.PROGRESS),
    (9, TodoStatus.COMPLETED),
])


class TodoParser(Parser):
    grammar = [
        Field('unused1?', 2, to_int),
        Field('type', 1, to_str),
        Field('space', 1, to_str),
        Field('descr', 150, to_str),
        Field('date1', 20, to_str),
        Field('date2', 20, to_str),
        # 1 = "event started date1 and ended date 2", 2 = "event between date1 and date2", 0 or empty = on date1
        Field('date_type', 1, to_str),
        Field('status', 1, to_str),
        Field('other_flags?', 8, to_str),
        Field('prio', 1, to_str),
        Field('other_flags?', 4, to_str),
        Field('loc_id', 8, to_int),
        Field('repo_id', 8, to_int),
        Field('unused2?', 85, to_str),
        Field('text_id', 8, to_int),
        Field('unused3?', 48, to_str),
    ]

    def handle(self, r, n, ref):
        loc = self.locations.get(r['loc_id'])
        repo = self.addresses.get(r['repo_id'])
        text = self.notes.get(r['text_id'])
        type = todo_type_map.get(r['type'])
        status = todo_status_map.get(r['status'])
        todo = Todo(date(r), type, status,
                    r['prio'], loc, repo, r['descr'], text)
        if not ref: # store global todo's locally
            ref = self
        ref.todos[n-1] = todo
        return todo
