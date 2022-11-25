from .field import Field, asterisk, to_int, to_str, modification_dates
from .parser import FileParser
from models import IntNote


class Notes(FileParser):
    fname = 'BKMessg.dt7'
    grammar = [
        Field('id', 9, to_int),
        Field('ref_type', 1, to_str),
        # 0 = person, 1 = family, 3 = source information, 5 = event, ...
        Field('ref_id', 9, to_int),
        Field('seq_nr', 3, to_int),
        Field('??1', 9, to_int),
        *modification_dates,
        Field('??2', 14, to_int),
        Field('next_seq_id', 9, to_int),
        Field('next_id', 9, to_int),
        Field('prev_id', 9, to_int),
        Field('start_marker', 1, asterisk),
        Field('text', 1200, to_str),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r):
        return r

    def read(self, dir):
        messages = {r['id']: r for r in self.rows(dir)}
        for (id, m) in messages.items():
            if m['seq_nr'] == 1:
                self[id] = self.note(messages, id)
        return self

    @classmethod
    def note(cls, messages, id):
        s = ''
        while id > 0:
            m = messages[id]
            s, id = s + m['text'], m['next_seq_id']
        return IntNote(s.replace('\x12\x13', '\n'))
