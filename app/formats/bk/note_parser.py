from .field import Field, to_int, to_str
from .parsers import Parser
from models import ExtNote


class NoteParser(Parser):
    grammar = [
        Field('path', 206, to_str),
        Field('print_where', 3, to_int),
        Field('unused1?', 100, to_str),
        Field('msg_id', 9, to_int),
        Field('unused2?', 48, to_str),
    ]

    def handle(self, r, n, ref):
        note = self.msgs.get_note(r['msg_id']) if r['msg_id'] else ExtNote(r['path'])
        if ref:
            ref.notes[n-1] = note
        else:
            print(f'WARNING: note without reference "{note}"')
        return note
