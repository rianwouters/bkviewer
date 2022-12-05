from .field import Field, asterisk, to_ids, to_int, to_str, modification_dates
from .parsers import FileParser
from models import Family


class FamiliesParser(FileParser):
    grammar = [
        Field('id', 8, to_int),
        Field('partner1_id', 8, to_int),
        Field('partner1_seq_nr', 3, to_int),
        Field('partner2_id', 8, to_int),
        Field('partner2_seq_nr', 3, to_int),
        Field('unused?', 4, to_str),
        Field('children_ids', 608, to_ids),
        *modification_dates,
        Field('??', 107, to_str),
        Field('next_id', 8, to_int),
        Field('next2_id', 8, to_int),
        Field('prev_id', 8, to_int),
        Field('prev2_id', 8, to_int),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r, persons):
        partners = [persons.get(r[p]) for p in ['partner1_id', 'partner2_id']]
        children = [persons[id] for id in r['children_ids']]
        family = Family(partners, children)
        for n, partner in enumerate(partners, 1):
            if partner:
                partner.families[r[f'partner{n}_seq_nr']-1] = family
        for child in children:
            child.parents.append(family)
        return family
