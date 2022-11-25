from .facts import Facts
from .field import Field, asterisk, to_int
from .files import Files
from .images import Images
from .medias import LocationData, Medias
from .names import Names
from .note import Note
from .parser import FileParser
from .todos import Todos
from .witnesses import Witnesses


class Others(FileParser):
    fname = 'BKOther.dt7'
    grammar = [
        Field('id', 9, to_int),
        Field('ref_type', 1, to_int),
        Field('ref_id', 9, to_int),
        Field('type', 1, to_int),
        Field('seq_nr', 3, to_int),
        Field('payload', 366, lambda s: s),
        Field('next_id', 9, to_int),
        Field('prev_id', 9, to_int),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, o, persons, families, events, sources, citations, locations, notes, addresses, todos):
        t = (o['ref_type'], o['type'])

        if t == (-1, -1):  # skip REUSE lines
            return None

        refs = [persons, families, self, events, self, events, self, self, [
                self, None, None, None, sources, citations, None, None, None, None][t[1]], locations][t[0]]
        cls_map = (
            (((0, 0), (1, 0)), Facts),
            (((0, 1),), Names),
            (((0, 2), (1, 2), (2, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0)), Note),
            (((0, 4), (1, 4)), Images),
            (((0, 7), (1, 7)), Medias),
            (((0, 8), (1, 8)), Todos),
            (((3, 0), (4, 0)), Witnesses),
            (((8, 4), (8, 5), (9, 4)), Files),
            (((9, 9),), LocationData),
        )
        try:
            handler_cls = next(filter(lambda m: t in m[0], cls_map))[1]
        except:
            raise Exception(f"Type combination {t} not implemented")
        handler = handler_cls(persons, locations, addresses, notes, todos)
        ref = refs.get(o['ref_id'])
        return handler.read(o['payload'], o['seq_nr'], ref)