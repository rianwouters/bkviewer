from .field import Field, to_int, to_str
from .parsers import Parser
from models import Witness, WitnessType


witness_type_map = dict([
    (0, WitnessType.WITNESS),
    (1, WitnessType.GODPARENT),
    (2, WitnessType.SPONSOR),
    (3, WitnessType.LEGAL_WITNESS),
    (4, WitnessType.INFORMANT),
    (5, WitnessType.PERSON_OF_HONOR),
    (9, WitnessType.OTHER),
])


class WitnessParser(Parser):
    grammar = [
        Field('type', 1, to_int),
        Field('unused1?', 4, to_int),
        Field('person_id', 8, to_int),
        Field('unused2?', 196, to_str),
        Field('extra_type', 100, to_str),
        Field('unused3?', 57, to_str),
    ]

    def handle(self, r, n, event):
        if r['person_id'] == -1:  # skip unused records
            # TODO clarify warning to specify if it refers to a person or family
            print(
                f'print(WARNING: invalid person for {event.type} event related to person/family {event.ref.id}')
            return None

        person = self.persons[r['person_id']]
        if r['type'] == -1:
            print(
                f'WARNING: no witness type defined for person #{r["person_id"]}')
            r['type'] = 0
        witness = Witness(person, event, witness_type_map[r['type']], r['extra_type'])
        event.witnesses[n-1] = witness
        return witness
