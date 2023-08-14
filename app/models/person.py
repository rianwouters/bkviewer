from models.name import Name, NameType
from .array import Array
from .str_enum import StrEnum


class Sexe(StrEnum):
    MAN = "Man"
    WOMAN = "Woman"
    UNKNOWN = "Unknown"


class PrivacyType(StrEnum):
    CLEAR = "No privacy settings"
    NAME_ONLY_DETAILS_BLANK = "Show name only, details blank"
    NAME_ONLY_DETAILS_PRIVATE = "Show name only, details 'private'"
    ALL_PRIVATE = "Show 'private' instead of name, details private"
    HIDE_PERSON = "Do not show that this person exists"


class Person:
    def __init__(self, id, sexe, fullname, firstname, surname, sortingname, title: PrivacyType, privacy, address=None):
        self.id = id
        self.sexe = sexe
        self.fullname = fullname
        self.firstname = firstname
        self.surname = surname
        self.sortingname = sortingname
        self.title = title
        self.privacy = privacy
        self.address = address
        self.families = Array("Families")
        self.parents = []
        self.notes = Array("Notes")
        self.events = Array("Events and Facts")
        self.media = Array("Media")
        self.images = Array("Images")
        self.names = Array("Names")
        self.todos = Array("Todo")
        self.citations = Array("General citations")
        self.name_citations = Array("Name citations")
        self.child_citations = Array("Child citations")
        self.names[0] = Name(NameType.FULL, fullname)

    @property
    def surname(self):
        return self._surname if self._surname else self.fullname.split(' ')[-1]

    @surname.setter
    def surname(self, surname):
        self._surname = surname

    def __str__(self) -> str:
        return f'Full name: {self.fullname}\nSexe: {self.sexe}{self.families}{self.events}{self.names}{self.notes}{self.images}{self.media}{self.citations}{self.name_citations}{self.child_citations}{self.todos}'
