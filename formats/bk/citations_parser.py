from .field import Field, asterisk, to_boolean, to_int, to_str, modification_dates
from .parsers import FileParser
from models import Citation


class CitationsParser(FileParser):
    grammar = [
        Field('id', 9, to_int),
        Field('ref_type', 1, to_int),
        Field('ref_id', 9, to_int),
        Field('type', 2, to_int),
        Field('seq_nr', 3, to_int),
        Field('source_id', 8, to_int),
        Field('descr', 100, to_str),
        # 3 = date and location, 2 = location only, 1 = date only, empty = unspecified
        Field('range', 1, to_int),
        Field('unused?', 50, to_int),
        Field('text_id', 9, to_int),
        Field('unused1?', 1, to_int),
        Field('info_id', 9, to_int),
        Field('unused2?', 1, to_int),
        Field('quality', 1, to_int),
        *modification_dates,
        Field('text_enabled', 1, to_boolean),
        Field('info_enabled', 1, to_boolean),
        Field('descr_enabled', 1, to_boolean),
        Field('unused3?', 27, to_str),
        Field('next_id', 9, to_int),
        Field('prev_id', 9, to_int),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r, msgs):
        return Citation(r['descr'], msgs.get_note(r['text_id']), msgs.get_note(r['info_id']))

    def rows(self):
        self.list = super().rows()
        return self.list

    def resolve(self, persons, families, events, others):
        refs = [persons, families, events, others,
                others, others, others, persons, others, others]
        for c in self.list:
            if c['ref_id'] > 0:
                t = [c['ref_type'], c['type']]
                ref = refs[t[0]][c['ref_id']]
                if t == [7, 0]:
                    list = ref.child_citations
                elif t == [0, 1]:
                    list = ref.name_citations
                else:
                    list = ref.citations
                list[c['seq_nr']] = self[c['id']]
        self.list = None
