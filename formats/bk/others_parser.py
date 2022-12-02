from .fact_parser import FactParser
from .field import Field, asterisk, to_int
from .file_ref_parser import FileRefParser
from .image_ref_parser import ImageRefParser
from .location_data_parser import LocationDataParser
from .media_ref_parser import MediaRefParser
from .name_parser import NameParser
from .note_parser import NoteParser
from .parsers import FileParser
from .todo_parser import TodoParser
from .witness_parser import WitnessParser


class OthersParser(FileParser):
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
            (((0, 0), (1, 0)), FactParser),
            (((0, 1),), NameParser),
            (((0, 2), (1, 2), (2, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0)), NoteParser),
            (((0, 4), (1, 4)), ImageRefParser),
            (((0, 7), (1, 7)), MediaRefParser),
            (((0, 8), (1, 8)), TodoParser),
            (((3, 0), (4, 0)), WitnessParser),
            (((8, 4), (8, 5), (9, 4)), FileRefParser),
            (((9, 9),), LocationDataParser),
        )
        try:
            handler_cls = next(filter(lambda m: t in m[0], cls_map))[1]
        except:
            raise Exception(f"Type combination {t} not implemented")
        handler = handler_cls(persons, locations, addresses, notes, todos)
        ref = refs.get(o['ref_id'])
        return handler.read(o['payload'], o['seq_nr'], ref)