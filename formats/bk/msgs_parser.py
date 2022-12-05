from .field import Field, asterisk, to_int, to_str, modification_dates, str_to_str_l, to_str_r, to_str_raw
from .parsers import FileParser
from models import IntNote

class MessageParser(FileParser):
    grammar = [
        Field('id', 9, to_int, to_str_r),
        Field('ref_type', 1, to_str, to_str_r),
        # 0 = person, 1 = family, 3 = source information, 5 = event, ...
        Field('ref_id', 9, to_int, to_str_r),
        Field('seq_nr', 3, to_int, to_str_r),
        Field('??1', 9, to_str, to_str_r),
        *modification_dates,
        Field('??2', 14, to_str, to_str_r),
        Field('next_seq_id', 9, to_int, to_str_r),
        Field('next_id', 9, to_int, to_str_r),
        Field('prev_id', 9, to_int, to_str_r),
        Field('start_marker', 1, asterisk, to_str_r),
        Field('text', 1200, to_str_raw, str_to_str_l),
        Field('end_marker', 1, asterisk, to_str_r),
    ]

    def convert(self, r):
        return r

    def remove_note(self, id):
        self._remove_note(id)

    def _note_messages(self, id):
        while id:
            m = self[id]
            id = m['next_seq_id']
            yield m

    def get_note(self, id):
        s = ''.join(m['text'] for m in self._note_messages(id))
        return IntNote(s.replace('\x12\x13', '\n').strip())

    def _remove_note(self, id):
        m = self[id]
        p, n = m['prev_id'], m['next_id']
        if p > 0:
            self[p]['next_id'] = n
        if n > 0:
            self[n]['prev_id'] = p
        for m in self._note_messages(id):
            m.update({
                'ref_type': None,
                'ref_id': None,
                'seq_nr': None,
                '??1': None,
                'date_added': None,
                'date_added_metadata': 0,
                'date_modified': None,
                'date_modified_metadata': None,
                '??2': None,
                'next_seq_id': None,
                'next_id': -1,
                'prev_id': -1,
                'text': "*REUSE*"
            })