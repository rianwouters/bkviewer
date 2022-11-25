from .array import Array
from .str_enum import StrEnum


class WitnessType(StrEnum):
    WITNESS = "witness"
    GODPARENT = "godparent"
    SPONSOR = "sponsor"
    LEGAL_WITNESS = "legal witness"
    INFORMANT = "informant"
    PERSON_OF_HONOR = "best man/maid of honor"
    OTHER = 'other'


class Witness:
    def __init__(self, person, type, extra_type) -> None:
        self.person = person
        self.type = type
        self.extra_type = extra_type
        self.citations = Array('Citations')

    def __str__(self) -> str:
        return f'{self.person.fullname} {self.type} {self.extra_type if self.extra_type else ""}'
