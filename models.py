from enum import Enum, unique


class Collection(dict):
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        lines = '\n'.join(str(l) for l in self.values())
        return f'\n{self.name}:\n{lines}\n' if lines else f'(No {self.name})'


class EventBase:
    def __init__(self, type, date):
        self.type = type
        self.date = date
        self.notes = Collection('Notes')
        self.witnesses = Collection("Witnesses")
        self.citations = Collection("Citations")

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
        self.notes = Collection('Notes')
        self.citations = Collection("Citations")

    def __str__(self) -> str:
        return f'{self.type}: {self.text} {self.date}'


class Witness:
    def __init__(self, person, type, extra_type) -> None:
        self.person = person
        self.type = type
        self.extra_type = extra_type
        self.citations = Collection('Citations')

    def __str__(self) -> str:
        return f'{self.person.fullname} {self.role} {self.extra_type if self.extra_type else ""}'


class Person:
    def __init__(self, id, sexe, fullname, firstname, surname, sortingname, title, privacy):
        self.id = id
        self.sexe = sexe
        self.fullname = fullname
        self.firstname = firstname
        self.surname = surname
        self.sortingname = sortingname
        self.title = title
        self.privacy = privacy
        self.families = Collection("Families")
        self.notes = Collection("Notes")
        self.events = Collection("Events and Facts")
        self.media = Collection("Media")
        self.images = Collection("Images")
        self.names = Collection("Names")
        self.todos = Collection("Todo")
        self.citations = Collection("General citations")
        self.name_citations = Collection("Name citations")
        self.child_citations = Collection("Child citations")

    def __str__(self) -> str:
        return f'Full name: {self.fullname}\nSexe: {self.sexe}{self.families}{self.events}{self.names}{self.notes}'


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
        return ' x '.join(fn) + f'{self.events}{self.notes}'


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
        return f'{super().__str__()}{self.notes}'


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


class StrEnum(Enum):
    def __init__(self, descr):
        self.descr = descr

    def __str__(self):
        return self.descr


class PrivacyTypes(StrEnum):
    CLEAR = "No privacy settings"
    NAME_ONLY_DETAILS_BLANK = "Show name only, details blank"
    NAME_ONLY_DETAILS_PRIVATE = "Show name only, details 'private'"
    ALL_PRIVATE = "Show 'private' instead of name, details private"
    HIDE_PERSON = "Do not show that this person exists"


class WitnessTypes(StrEnum):
    WITNESS = "witness"
    GODPARENT = "godparent"
    SPONSOR = "sponsor"
    LEGAL_WITNESS = "legal witness"
    INFORMANT = "informant"
    PERSON_OF_HONOR = "best man/maid of honor"
    OTHER = 'other'


class NameTypes(StrEnum):
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


class EventTypes(StrEnum):
    BORN = 'Born'
    BAPTIZED = 'Baptized'
    CHRISTENED = 'Christened'
    DIED = 'Died'
    BURRIED = 'Burried'
    CREMATED = 'Cremated'
    ADOPTED_BY_BOTH = 'Adopted by both'
    ADOPTED_BY_FATHER = 'Adopted by father'
    ADOPTED_BY_MOTHER = 'Adopted by mother'
    BAPTIZED_LDS = 'Baptized LDS'
    BAR_MITZVAH = 'Bar Mitzvah'
    BLESSING = 'Blessing'
    BRIT_MILAH = 'Brit Milah'
    CENSUS = 'Census'
    CHRISTENED_ADULT = 'Christened (adult)'
    CONFIRMATION = 'Confirmation'
    CONFIRMATION_LDS = 'Confirmation LDS'
    EMIGRATED = 'Emigrated'
    ENDOWMENT_LDS = 'Endowment LDS'
    EVENT = 'Event'
    FIRST_COMMUNION = 'First Communion'
    FUNERAL = 'Funeral'
    GRADUATED = 'Graduated'
    IMIGRATED = 'Immigrated'
    INTERRED = 'Interred'
    NATURALIZED = 'Naturalized'
    ORDNINATION = 'Ordination'
    PROBATE = 'Probate'
    RETIREMENT = 'Retirement'
    RESIDED = 'Resided'
    SEALED_CHILD_LDS = 'Sealed child LDS'
    WILL_SIGNED = 'Will signed'
    VARTZEIT = 'Yartzeit'
    VERIFY_HOME_CHRISTENING = 'Verify home christening'
    CHURCHING_OF_WOMAN = 'Churching of woman'
    MEMORIAL_SERVICE = 'Memorial serivce'
    NOT_LIVING = 'Not living'
    NEVER_MARRIED = 'Never married'
    NO_CHILDREN_FROM_PERSON = 'No children from this person'
    OCCUPATION = 'Occupation'
    MILITARY = 'Military'
    RELIGION = 'Religion'
    EDUCATION = 'Education'
    NATIONALITY = 'Nationality'
    CASTE = 'Caste'
    REF_NUMBER = 'Ref number'
    AFN_NUMER = 'AFN number'
    SOCIAL_SECURITY_NUMBER = 'Social Security Number'
    PERMANENT_NUMBER = 'Permanent number'
    ID_NUMBER = 'ID number'
    Y_DNA = 'Y-DNA'
    MT_DNA = 'mtDNA'
    AT_DNA = 'atDNA'
    LEGAL_NAME_CHANGE = 'Legal name change'
    HEIGHT = 'Height'
    WEIGHT = 'Weight'
    EYE_COLOR = 'Eye color'
    HAIR_COLOR = 'Hair color'
    DESCRIPTION = 'Description'
    PROPERTY = 'Property'
    MEDICAL_CONDITION = 'Medical condition'
    CAUSE_OF_DEATH = 'Cause of death'
    NUMBER_OF_CHILDREN_PERSON = 'Number of children (person)'
    ANCESTOR_INTEREST = 'Ancestor interest'
    DESCENDANT_INTEREST = 'Descendant interest'
    MARRIED = 'Married'
    MARRIED_CIVIL = 'Married (civil)'
    MARRIED_RELIGIOUS = 'Married (religious)'
    DIVORCED = 'Divorced'
    MARRIED_BANN = 'Married Bann'
    MARRIAGE_BOND = 'Marriage Bond'
    MARRIAGE_CONTRACT = 'Marriage contract'
    MARRIAGE_LICENSE = 'Marriage license'
    MARRIAGE_SETTLEMENT = 'Marriage settlement'
    MARRIAGE_INTENTION = 'Marriage intention'
    DIVORCE_FILED = 'Divorce filed'
    SEPARATED = 'Separated'
    ANULLED = 'Annulled'
    ENGAGED = 'Engaged'
    SEALED_TO_SPOUSE_LDS = 'Sealed to spouse LDS'
    RESIDED_FAMILY = 'Resided (family)'
    EVENT_FAMILY = 'Event (family)'
    CENSUS_FAMILY = 'Census (family)'
    NOT_MARRIED = 'Not married'
    COMMON_LAW = 'Common law'
    NO_CHILDREN_FROM_THIS_MARRIAGE = 'No children from this marriage'
    NUMBER_OF_CHILDREN_FAMILY = 'Number of Children (family)'
    MARRIAGE_ID = 'Marriage ID number'
    MARRIAGE_REF = 'Marriage Reference number'


class Sexe(StrEnum):
    MAN = "Man"
    WOMAN = "Woman"
    UNKNOWN = "Unknown"
