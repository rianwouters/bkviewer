class Collection(dict):
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        lines = '\n'.join(str(l) for l in self.values())
        return f'{self.name}:\n{lines}\n'


class EventBase:
    def __init__(self, name, date):
        self.name = name
        self.date = date
        self.notes = Collection('Notes')
        self.witnesses = Collection("Witnesses")
        self.citations = Collection("Citations")

    def __str__(self):
        return f'{self.type} {self.date}\n{self.notes}\n{self.witnesses}'


class Event(EventBase):
    def __init__(self, name, date, prepos, loc):
        super().__init__(name, date)
        self.prepos = prepos
        self.loc = loc

    def __str__(self):
        witnesses = '\n'.join(f'   {w}' for w in self.witnesses.values())
        return f'{self.name} {self.date} {self.loc}\n{self.notes}\n{witnesses}'


class Fact(EventBase):
    def __init__(self, name, date, descr):
        super().__init__(name, date)
        self.descr = descr

    def __str__(self):
        return f'{self.name}: {self.descr} {self.date}\n{self.notes}\n{self.witnesses}'


class Name:
    def __init__(self, type, text, date):
        self.type = type
        self.text = text
        self.date = date
        self.notes = Collection('Notes')
        self.citations = Collection("Citations")

    def __str__(self) -> str:
        return f'{self.type} {self.text} {self.date}'


class Witness:
    def __init__(self, person, role, other_role) -> None:
        self.person = person
        self.role = role
        self.other_role = other_role
        self.citations = Collection('Citations')

    def __str__(self) -> str:
        return f'{self.person.fullname} {self.role} {self.other_role} '

# shortcut to initialize the object in p named 'self' with attributes k with value v for all other values in p
# so that init(locals()) initializes all object attributes based on the __init__ parameters


class Person:
    def __init__(self, id, fullname, firstname, surname, sortingname, title):
        self.id = id
        self.fullname = fullname
        self.firstname = firstname
        self.surname = surname
        self.sortingname = sortingname
        self.title = title
        self.families = {}
        self.notes = Collection("Notes")
        self.events = Collection("Events")
        self.media = Collection("Media")
        self.images = Collection("Images")
        self.names = Collection("Names")
        self.todos = Collection("Todo")
        self.citations = Collection("General citations")
        self.name_citations = Collection("Name citations")
        self.child_citations = Collection("Child citations")

    def __str__(self) -> str:
        families = '\n'.join(str(f) for f in self.families.values())
        return f'Full name: {self.fullname}\nFamilies:\n{families}\n{self.events}\n{self.notes}\n{self.names}'


class Family:
    def __init__(self, partners, children):
        self.partners = partners
        self.children = children
        self.notes = Collection("Notes")
        self.events = Collection("Events")
        self.media = Collection("Media")
        self.images = Collection("Images")
        self.citations = Collection("Citations")

    def __str__(self) -> str:
        fn = map(lambda p: p.fullname if p else "(empty)", self.partners)
        return ' x '.join(fn) + f'\n{self.events}\n{self.notes}'


class Note:
    def __init__(self) -> None:
        self.citations = Collection("Citations")


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
        self.notes = Collection('Notes')
        self.citations = Collection('Citations')

    def __str__(self) -> str:
        return f'{super().__str__()}\n{self.notes}'


class Image(Media):
    def __init__(self, path, descr, dimensions, print_where) -> None:
        super().__init__(path, descr)
        self.dimensions = dimensions
        self.print_where = print_where


class Todo:
    def __init__(self, status, prio, loc, arch, descr, text) -> None:
        self.status = status
        self.prio = prio
        self.loc = loc
        self.arch = arch
        self.descr = descr
        self.note = None

    def __str__(self) -> str:
        return f'{self.status} {self.prio} {self.loc} {self.arch} {self.descr} {self.text}'


class Source:
    def __init__(self, title, text, note):
        self.title = title
        self.text = text
        self.note = note
        self.files = Collection('Files')

    def __str__(self) -> str:
        return self.title


class Citation:
    def __init__(self, descr, type, text=None, info=None):
        self.descr = descr
        self.text = text
        self.info = info
        self.files = Collection('Files')


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
        self.notes = Collection("Notes")
        self.files = Collection("Files")

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
