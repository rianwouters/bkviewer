from .array import Array
from .str_enum import StrEnum


class NameType(StrEnum):
    ALSO_KNOWN_AS = 'Also known as'
    NICK = 'Nickname'
    SHORT = 'Short name'
    ADOPTED = 'Adopted name'
    HEBREW = 'Hebrew name'
    CENSUS = 'Census'
    MARIIED = 'Married name'
    GERMAN = 'German name'
    FARM = 'Farm name'
    BIRTH = 'Birth name'
    INDIAN = 'Indian name'
    FORMAL = 'Formal name'
    CURRENT = 'Current name'
    SOLDIER = 'Soldier name'
    FORMERLY_KNOWN_AS = 'Formerly known as'
    RELIGIOUS = 'Religious name'
    CALLED = 'Called'
    INDIGENOUS = 'Indigenous name'
    TOMBSTONE = 'Tombstone name'
    OTHER = 'Other name'


class Name:
    def __init__(self, type, text, date):
        self.type = type
        self.text = text
        self.date = date
        self.notes = Array('Notes')
        self.citations = Array("Citations")

    def __str__(self) -> str:
        return f'{self.type}: {self.text} {self.date}'
