from enums import EventType


class Array(list):

    def __init__(self, name):
        self.name = name

    def _ensure_length(self, n):
        l = len(self)
        if n > l:
            self.extend([None]*(n - l))

    def __setitem__(self, n, val):
        self._ensure_length(n + 1)
        list.__setitem__(self, n, val)

    def __str__(self) -> str:
        lines = '\n'.join(str(l) for l in self)
        return f'\n{self.name}:\n{lines}\n' if lines else f'\n(No {self.name})'

class Collection(dict):
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        lines = '\n'.join(str(l) for l in self.values())
        return f'\n{self.name}:\n{lines}\n' if lines else f'\n(No {self.name})'


class EventBase:
    def __init__(self, type: EventType, date):
        self.type = type
        self.date = date
        self.notes = Array('Notes')
        self.witnesses = Array("Witnesses")
        self.citations = Array("Citations")

    def __str__(self):
        return f'{self.type} {self.date}{self.notes}{self.witnesses}'


class Event(EventBase):
    def __init__(self, type, date, prepos, loc):
        super().__init__(type, date)
        self.prepos = prepos
        self.loc = loc

    def __str__(self):
        return f'{self.type} {self.loc} {self.date}{self.notes}{self.witnesses}'


class Fact(EventBase):
    def __init__(self, type, date, descr):
        super().__init__(type, date)
        self.descr = descr

    def __str__(self):
        return f'{self.type} {self.descr} {self.date}{self.notes}{self.witnesses}'


class Name:
    def __init__(self, type, text, date):
        self.type = type
        self.text = text
        self.date = date
        self.notes = Array('Notes')
        self.citations = Array("Citations")

    def __str__(self) -> str:
        return f'{self.type}: {self.text} {self.date}'


class Witness:
    def __init__(self, person, type, extra_type) -> None:
        self.person = person
        self.type = type
        self.extra_type = extra_type
        self.citations = Array('Citations')

    def __str__(self) -> str:
        return f'{self.person.fullname} {self.type} {self.extra_type if self.extra_type else ""}'


class Person:
    def __init__(self, id, sexe, fullname, firstname, surname, sortingname, title, privacy, address=None):
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

    def __str__(self) -> str:
        return f'Full name: {self.fullname}\nSexe: {self.sexe}{self.families}{self.events}{self.names}{self.notes}{self.images}{self.media}{self.citations}{self.name_citations}{self.child_citations}{self.todos}'

    def set_family(self, n, f):
        l = len(self.families)
        if n >= l:
            self.families.extend((None)*(n + 1 - l))
        else:
            if self.families[n]:
                print("")
        self.families[n] = f


class Family:
    def __init__(self, partners, children, address=None):
        self.partners = partners
        self.children = children
        self.address = address
        self.notes = Array("Notes")
        self.events = Array("Events")
        self.media = Array("Media")
        self.images = Array("Images")
        self.citations = Array("Citations")

    def __str__(self) -> str:
        fn = map(lambda p: p.fullname if p else "(empty)", self.partners)
        return ' x '.join(fn) + f'{self.events}{self.notes}{self.images}{self.media}{self.citations}'


class Note:
    def __init__(self) -> None:
        self.citations = Array("Citations")


class ExtNote(Note):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def __str__(self) -> str:
        return self.path


class IntNote(Note):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        return self.text


class File:
    def __init__(self, path, descr) -> None:
        self.path = path
        self.descr = descr

    def __str__(self) -> str:
        return f'{self.path} {self.descr}'


class Media(File):
    def __init__(self, path, descr) -> None:
        super().__init__(path, descr)
        self.notes = Array('Notes')
        self.citations = Array('Citations')

    def __str__(self) -> str:
        return f'{super().__str__()}{self.notes}'


class Image(Media):
    def __init__(self, path, descr, dimensions, print_where) -> None:
        super().__init__(path, descr)
        self.dimensions = dimensions
        self.print_where = print_where


class Todo:
    def __init__(self, date, type, status, prio, loc, arch, descr, text) -> None:
        self.date = date
        self.type = type
        self.status = status
        self.prio = prio
        self.loc = loc
        self.arch = arch
        self.descr = descr
        self.text = text
        self.note = None

    def __str__(self) -> str:
        return f'{self.status} {self.prio} {self.loc} {self.arch} {self.descr} {self.text}'


class Source:
    def __init__(self, title, text, note):
        self.title = title
        self.text = text
        self.note = note
        self.files = Array('Files')

    def __str__(self) -> str:
        return self.title


class Citation:
    def __init__(self, descr, type, text=None, info=None):
        self.descr = descr
        self.text = text
        self.info = info
        self.files = Array('Files')


class Location:
    def __init__(self, name, short_name=None, city=None, township=None, county=None,  state_or_province=None, country=None, latitude=None, longitude=None, farm_or_manor_name=None, parish=None, postal_address=None, resident_id=None, residence_number=None, farm_number=None, property_number=None):
        self.name = name
        self.short_name = short_name
        self.city = city
        self.township = township
        self.county = county
        self.state_or_province = state_or_province
        self.country = country
        self.latitude = latitude
        self.longitude = longitude
        self.farm_or_manor_name = farm_or_manor_name
        self.parish = parish
        self.postal_address = postal_address
        self.resident_id = resident_id
        self.residence_number = residence_number
        self.farm_number = farm_number
        self.property_number = property_number
        self.notes = Array("Notes")
        self.files = Array("Files")

    def __str__(self) -> str:
        return self.name


class Address:
    def __init__(self, fullname, line1, line2, line3, line4, phone, fax, email, web):
        self.fullname = fullname
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3
        self.line4 = line4
        self.phone = phone
        self.fax = fax
        self.web = web
        self.email = email


class Genealogy:
    pass
