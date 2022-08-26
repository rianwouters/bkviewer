from asyncio import Handle
from audioop import add
from datetime import datetime
from fnmatch import fnmatch
from os.path import join
from itertools import accumulate
from models import Event, ExtNote, Fact, File, Genealogy, Image, IntNote, Media, Name, Person, Location, Source, Citation, Family, Address, Todo, Witness
from maps import sexe_type_map, privacy_type_map, event_type_map, name_type_map, witness_type_map, todo_type_map, todo_status_map
from dates import create_date


class Field:
    def __init__(self, name, len, fn):
        self.name = name
        self.len = len
        self.fn = fn


def _date(row):
    return create_date(row['date1'], row['date2'], row['date_type'])


def to_boolean(s):
    return s == '1'


def to_int(s):
    try:
        return -1 if s.strip() == '' or s == '\x00' else int(s)
    except:
        return s


def to_str(s):
    return s.strip()


def to_date(s):
    try:
        return datetime.strptime(s, "%Y%m%d")
    except:
        return None


def to_ids(s):
    for n in range(0, len(s), 8):
        id = to_int(s[n:n+8])
        if id < 0:
            break
        yield id


def asterisk(s):
    if s == '*':
        return s
    raise Exception(f"Parsing error: {s} (expected '*')")


_modification_dates = [
    Field('date_added', 8, to_date),
    # 5 means converted from BK5 which did not have this data, so it was converted from the modification date
    Field('date_added_metadata', 4, to_int),
    Field('date_modified', 8, to_date),
    # 5 means converted from BK5 so it may be the same as the added date
    Field('date_modified_metadata', 4, to_int),
]


def _parse(s, grammar):
    pos = accumulate(grammar, lambda t, f: t + f.len, initial=0)
    return {f.name: f.fn(s[n:n+f.len]) for f, n in zip(grammar, pos)}


class FileParser(dict):

    def read(self, dir, *args):
        for r in self.rows(dir):
            self[r['id']] = self.convert(r, *args)
        return self

    # TODO this fails if end of lines or incorrectly mixed up as \x0d \x0d \x0a for example
    # seems to work in most cases but for some reasons sometimes an extra \x0a ends up in some files
    def rows(self, dir):
        with open(join(dir, self.fname)) as f:
            lines = f.readlines()
        n = 0
        while n < len(lines):
            bkline = lines[n]
            n += 1
            while bkline[-2] != "*":
                bkline += '\n' + lines[n]
                n += 1
            yield _parse(bkline, self.grammar)


class Parser():
    def __init__(self, persons, locations, addresses ,notes):
        self.persons = persons
        self.locations = locations
        self.addresses = addresses
        self.notes = notes

    def read(self, s, n, ref):
        return self.handle(_parse(s, self.grammar), n, ref)


class Notes(FileParser):
    fname = 'BKMessg.dt7'
    grammar = [
        Field('id', 9, to_int),
        Field('ref_type', 1, to_str),
        # 0 = person, 1 = family, 3 = source information, 5 = event, ...
        Field('ref_id', 9, to_int),
        Field('seq_nr', 3, to_int),
        Field('??1', 9, to_int),
        *_modification_dates,
        Field('??2', 14, to_int),
        Field('next_seq_id', 9, to_int),
        Field('next_id', 9, to_int),
        Field('prev_id', 9, to_int),
        Field('start_marker', 1, asterisk),
        Field('text', 1200, to_str),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r):
        return r

    def read(self, dir):
        messages = {r['id']: r for r in self.rows(dir)}
        for (id, m) in messages.items():
            if m['seq_nr'] == 1:
                self[id] = self.note(messages, id)
        return self

    @classmethod
    def note(cls, messages, id):
        s = ''
        while id > 0:
            m = messages[id]
            s, id = s + m['text'], m['next_seq_id']
        return IntNote(s.replace('\x12\x13', '\n'))


class Locations(FileParser):
    fname = 'BKLocate.dt7'
    grammar = [
        Field('id', 8, to_int),
        Field('name', 120, to_str),
        Field('short_name', 41, to_str),
        Field('city', 40, to_str),
        Field('township', 40, to_str),
        Field('county', 40, to_str),
        Field('state_or_province', 40, to_str),
        Field('country', 40, to_str),
        Field('ref_id??', 8, to_int),
        Field('latitude', 15, to_str),
        Field('longitude', 15, to_str),
        Field('loc_data_id', 8, to_int),
        Field('next_id', 8, to_int),
        Field('prev_id', 8, to_int),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r):
        return Location(r['name'], r['city'], r['township'], r['county'],
                        r['state_or_province'], r['country'], r['latitude'], r['longitude'])


class Sources(FileParser):
    fname = 'BKSource.dt7'
    grammar = [
        Field('id', 8, to_int),
        Field('title', 129, to_str),
        Field('media', 1, to_str),
        Field('abbreviation', 120, to_str),
        Field('author', 120, to_str),
        Field('publisher_year', 120, to_str),
        Field('repo_id', 8, to_int),
        Field('??1', 9, to_str),
        Field('archive_access_number', 80, to_str),
        Field('??', 27, to_str),
        Field('text_id', 9, to_int),
        Field('??', 1, to_str),
        Field('info_id', 9, to_int),
        Field('??2', 1, to_str),
        Field('??3', 61, to_str),
        *_modification_dates,
        Field('title_enabled', 1, to_boolean),
        Field('author_enabled', 1, to_boolean),
        Field('publisher_year_enabled', 1, to_boolean),
        Field('abbreviation_enabled', 1, to_boolean),
        Field('print_text', 1, to_boolean),
        Field('print_info', 1, to_boolean),
        Field('parenthesis', 1, to_boolean),
        Field('italics', 1, to_boolean),
        Field('??', 38, to_str),
        Field('next_id', 8, to_int),
        Field('prev_id', 8, to_int),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r, notes):
        return Source(r['title'], notes.get(r['text_id']), notes.get(r['info_id']))


class Citations(FileParser):
    fname = 'BKSourPT.dt7'
    grammar = [
        Field('id', 9, to_int),
        Field('ref_type', 1, to_int),
        Field('ref_id', 9, to_int),
        Field('type', 2, to_int),
        Field('seq_nr', 3, to_int),
        Field('source_id', 8, to_int),
        Field('descr', 100, to_str),
        # 3 = date and location, 2 = location only, 1 = date only, empty = unspecified
        Field('range', 1, to_int),
        Field('unused?', 50, to_int),
        Field('text_id', 9, to_int),
        Field('unused1?', 1, to_int),
        Field('info_id', 9, to_int),
        Field('unused2?', 1, to_int),
        Field('quality', 1, to_int),
        *_modification_dates,
        Field('text_enabled', 1, to_boolean),
        Field('info_enabled', 1, to_boolean),
        Field('descr_enabled', 1, to_boolean),
        Field('unused3?', 27, to_str),
        Field('next_id', 9, to_int),
        Field('prev_id', 9, to_int),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r, notes):
        return Citation(r['descr'], notes.get(r['text_id']), notes.get(r['info_id']))

    def rows(self, dir):
        self.list = super().rows(dir)
        return self.list

    def resolve(self, persons, families, events, others):
        refs = [persons, families, events, others,
                others, others, others, persons, others, others]
        for c in self.list:
            if c['ref_id'] > 0:
                t = [c['ref_type'], c['type']]
                ref = refs[t[0]][c['ref_id']]
                if t == [7, 0]:
                    list = ref.child_citations
                elif t == [0, 1]:
                    list = ref.name_citations
                else:
                    list = ref.citations
                list[c['seq_nr']] = self[c['id']]
        self.list = None


class Persons(FileParser):
    fname = 'BKPerson.dt7'
    grammar = [
        Field('id', 8, to_int),
        Field('surname_prefix_5caps', 5, to_str),
        Field('firstname_prefix_5caps', 5, to_str),
        Field('fullname', 140, to_str),
        Field('surname_prefix_10caps', 10, to_str),
        Field('firstname_prefix_10caps', 10, to_str),
        Field('unknown1', 40, to_str),
        Field('prefix', 40, to_str),
        Field('postfix', 40, to_str),
        Field('firstname', 40, to_str),
        Field('surname', 40, to_str),
        Field('sortingname', 40, to_str),
        Field('title', 50, to_str),
        Field('sexe', 2, to_int),
        Field('parents_family_id1', 8, to_int),
        Field('parents_family_id2', 8, to_int),
        Field('unknown2', 8, to_str),
        Field('unknown3', 8, to_str),
        Field('parents1_types', 1, to_int),
        Field('parents2_types', 1, to_int),
        Field('??', 8, to_int),
        *_modification_dates,
        Field('empty?', 8, to_str),
        Field('privacy', 1, to_int),
        Field('unknown4', 76, to_str),
        Field('groups', 10, to_str),
        Field('unknown5', 5, to_str),
        Field('default_family_id', 1, to_str),
        Field('unknown6', 25, to_str),
        Field('find_a_grave', 12, to_str),
        Field('i1', 8, to_int),
        Field('i2', 8, to_int),
        Field('i3', 8, to_int),
        Field('i4', 8, to_int),
        Field('i5', 8, to_int),
        Field('i6', 8, to_int),
        Field('i7', 8, to_int),
        Field('i8', 8, to_int),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r):
        return Person(r['id'], sexe_type_map[r['sexe']], r['fullname'], r['firstname'], r['surname'], r['sortingname'], r['title'], privacy_type_map[r['privacy']])


class Families(FileParser):
    fname = 'BKMarr.dt7'
    grammar = [
        Field('id', 8, to_int),
        Field('partner1_id', 8, to_int),
        Field('partner1_seq_nr', 3, to_int),
        Field('partner2_id', 8, to_int),
        Field('partner2_seq_nr', 3, to_int),
        Field('unused?', 4, to_str),
        Field('children_ids', 608, to_ids),
        *_modification_dates,
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
                partner.families[r[f'partner{n}_seq_nr']] = family
        for child in children:
                child.parents.append(family)
        return family


class Addresses(FileParser):
    fname = 'BKMail.dt7'
    grammar = [
        Field('id', 8, to_int),
        Field('ref_type', 1, to_int),
        Field('ref_id', 8, to_str),
        Field('type', 3, to_str),
        Field('cs_surname_firstname', 30, to_str),
        Field('fullname', 60, to_str),
        Field('line1', 60, to_str),
        Field('line2', 60, to_str),
        Field('line3', 60, to_str),
        Field('line4', 60, to_str),
        Field('phone', 60, to_str),
        Field('fax', 60, to_str),
        Field('email', 60, to_str),
        Field('web', 60, to_str),
        Field('other', 60, to_str),
        Field('holiday_list', 1, to_int),
        Field('birthday_list', 1, to_int),
        Field('reunion_list', 1, to_int),
        Field('newsletter', 1, to_int),
        Field('other1_list', 1, to_int),
        Field('other2_list', 1, to_int),
        Field('other3_list', 1, to_int),
        Field('unused', 1, to_int),
        Field('unused', 1, to_int),
        Field('unused', 1, to_int),
        Field('unused1?', 179, to_str),
        *_modification_dates,
        Field('unused2?', 16, to_str),
        Field('next_id', 8, to_str),
        Field('prev_id', 8, to_str),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r, persons, families, repos):
        address = Address(r['fullname'], r['line1'], r['line2'], r['line3'],
                          r['line4'], r['phone'], r['fax'], r['email'], r['web'])
        type, id = r['ref_type'], r['ref_id']
        if type < 0:  # skip REUSE lines
            return
        if type < 2:
            [persons, families][type][int(id)].address = address
        else:
            repos[id] = address
        return address


class Events(FileParser):
    fname = 'BKEvent.dt7'
    grammar = [
        Field('id', 9, to_int),
        Field('ref_type', 1, to_int),
        Field('ref_id', 8, to_int),
        # type ref-type-specific sequence number shared with 'other' events
        Field('seq_nr', 3, to_int),
        Field('type', 3, to_int),
        Field('prepos', 2, to_int),
        Field('date1', 20, to_str),
        Field('date2', 20, to_str),
        Field('loc_id', 8, to_int),
        # 1 = "event started date1 and ended date2", 2 = "event between date1 and date2", 0 or empty = on date1
        Field('date_type', 9, to_int),
        # seems always empty
        Field('??1', 30, to_str),
        # for families: partner-specific event sequence number, shared with 'other' events?
        Field('partner1_seq_nr', 3, to_int),
        Field('partner2_seq_nr', 3, to_int),
        # seems always empty
        Field('??2', 6, to_str),
        Field('custom_name', 18, to_str),
        Field('next_id', 9, to_int),
        Field('prev_id', 9, to_int),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r, persons, families, locations):
        refs = [persons, families]
        if r['ref_id'] > 0:  # skip reuse events
            loc = locations.get(r['loc_id'])
            name = r['custom_name']
            event = Event(
                name if name else event_type_map[r['type']], _date(r), r['prepos'], loc)
            ref = refs[r['ref_type']][r['ref_id']]
            ref.events[r['seq_nr']] = event
            return event


class Facts(Parser):
    grammar = [
        Field('type', 3, to_int),
        Field('space', 1, to_str),
        Field('descr', 150, to_str),
        Field('date1', 20, to_str),
        Field('date2', 20, to_str),
        # 1 = "event started date1 and ended date 2", 2 = "event between date1 and date2", 0 or empty = on date1
        Field('date_type', 1, to_str),
        Field('unused1?', 123, to_str),
        Field('custom_name', 18, to_str),
        Field('unused2?', 30, to_str),
    ]

    def handle(self, r, n, ref):
        name = r['custom_name']
        fact = Fact(
            name if name else event_type_map[r['type']], _date(r), r['descr'])
        ref.events[n] = fact
        return fact


class Names(Parser):
    grammar = [
        Field('type', 3, to_int),
        Field('space', 1, to_str),
        Field('text', 150, to_str),
        Field('date1', 20, to_str),
        Field('date2', 20, to_str),
        # 1 = "event started date1 and ended date 2", 2 = "event between date1 and date2", 0 or empty = on date1
        Field('date_type', 1, to_str),
        Field('unused1?', 11, to_str),
        Field('print_where', 3, to_int),
        Field('unused2?', 157, to_str),
    ]

    def handle(self, r, n, ref):
        name = Name(name_type_map[r['type']], r['text'], _date(r))
        ref.names[n] = name
        return name


class Note(Parser):
    grammar = [
        Field('path', 206, to_str),
        Field('print_where', 3, to_int),
        Field('unused1?', 100, to_str),
        Field('msg_id', 9, to_int),
        Field('unused2?', 48, to_str),
    ]

    def handle(self, r, n, ref):
        note = self.notes.get(r['msg_id'], ExtNote(r['path']))
        if ref:
            ref.notes[n] = note
        else:
            print(f'WARNING: note without reference "{note}"')
        return note


class Images(Parser):
    grammar = [
        Field('space', 4, to_str),
        Field('path', 150, to_str),
        Field('unused1?', 47, to_str),
        Field('dimensions', 2, to_str),
        Field('unused2?', 3, to_str),
        Field('print_where', 3, to_str),
        Field('descr', 100, to_str),
        Field('unused2?', 57, to_str),
    ]

    def handle(self, r, n, ref):
        image = Image(r['path'], r['descr'], r['dimensions'], r['print_where'])
        ref.images[n] = image
        return image


class Todos(Parser):
    grammar = [
        Field('unused1?', 2, to_int),
        Field('type', 1, to_str),
        Field('space', 1, to_str),
        Field('descr', 150, to_str),
        Field('date1', 20, to_str),
        Field('date2', 20, to_str),
        # 1 = "event started date1 and ended date 2", 2 = "event between date1 and date2", 0 or empty = on date1
        Field('date_type', 1, to_str),
        Field('status', 1, to_str),
        Field('other_flags?', 8, to_str),
        Field('prio', 1, to_str),
        Field('other_flags?', 4, to_str),
        Field('loc_id', 8, to_int),
        Field('repo_id', 8, to_int),
        Field('unused2?', 85, to_str),
        Field('text_id', 8, to_int),
        Field('unused3?', 48, to_str),
    ]

    def handle(self, r, n, ref):
        loc = self.locations.get(r['loc_id'])
        repo = self.addresses.get(r['repo_id'])
        text = self.notes.get(r['text_id'])
        type = todo_type_map.get(r['type'])
        status = todo_status_map.get(r['status'])
        todo = Todo(_date(r), type, status,
                    r['prio'], loc, repo, r['descr'], text)
        if ref:  # skip global todo's
            ref.todos[n] = todo
        else:
            print(
                f'WARNING: skipping global to do item: "{todo.descr}"')
        return todo


class Witnesses(Parser):
    grammar = [
        Field('type', 1, to_int),
        Field('unused1?', 4, to_int),
        Field('person_id', 8, to_int),
        Field('unused2?', 196, to_str),
        Field('extra_type', 100, to_str),
        Field('unused3?', 57, to_str),
    ]

    def handle(self, r, n, ref):
        if r['person_id'] == -1: # skip unused records
            return None

        person = self.persons[r['person_id']]
        if r['type'] == -1:
            print(
                f'WARNING: no witness type defined for person #{r["person_id"]}')
            r['type'] = 0
        witness = Witness(
            person, witness_type_map[r['type']], r['extra_type'])
        ref.witnesses[n] = witness
        return witness


class Files(Parser):
    grammar = [
        Field('space', 4, to_str),
        Field('path', 150, to_str),
        Field('unused1?', 52, to_str),
        Field('unused2?', 3, to_int),
        Field('descr', 100, to_str),
        Field('unused3', 57, to_str),
    ]

    def handle(self, r, n, ref):
        file = File(r['path'], r['descr'])
        ref.files[n] = file
        return file


class Medias(Files):
    def handle(self, r, n, ref):
        media = Media(r['path'], r['descr'])
        ref.media[n] = media
        return media


class LocationData(Parser):
    grammar = [
        Field('space', 4, to_str),
        Field('farm_or_manor_name', 40, to_str),
        Field('parish', 40, to_str),
        Field('postal_address', 125, to_str),
        Field('resident_id', 25, to_str),
        Field('residence_number', 25, to_str),
        Field('farm_number', 25, to_str),
        Field('property_number', 25, to_str),
        Field('unused?', 57, to_str),
    ]

    def handle(self, r, n, ref):
        ref.farm_or_manor_name = r['farm_or_manor_name']
        ref.parish = r['parish']
        ref.postal_address = r['postal_address']
        ref.resident_id = r['resident_id']
        ref.residence_number = r['residence_number']
        ref.farm_number = r['farm_number']
        ref.property_number = r['property_number']
        return ref


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

    def convert(self, o, persons, families, events, sources, citations, locations, notes, addresses):
        t = (o['ref_type'], o['type'])

        if t == (-1, -1): # skip REUSE lines
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
        handler = handler_cls(persons, locations, addresses ,notes)
        ref = refs.get(o['ref_id'])
        return handler.read(o['payload'], o['seq_nr'], ref)


# Reading order is determined as follows:
# - locations has to go before events, others
# - sources has to go before citations
# - citations has to go before others
# - persons have to go before families, adresses, events, others, citations
# - families has to go before adresses, events, others, citations
# - addresses have to go before others
# - events have to go before others, citations
# - others have to go before citations
#
# The only cycle in here is others -> citations -> others
# A "read as late as possible" strategy leads to the following order:
#  persons, families, locations, events, sources, citations, addresses, others
# Citation references will he resolved as a separate step in the end.
def read(dir):
    g = Genealogy()
    g.notes = Notes().read(dir)
    g.locations = Locations().read(dir)
    g.sources = Sources().read(dir, g.notes)
    g.citations = Citations().read(dir, g.notes)
    g.persons = Persons().read(dir)
    g.families = Families().read(dir, g.persons)
    g.repositories = {}
    g.addresses = Addresses().read(dir, g.persons, g.families, g.repositories)
    g.events = Events().read(dir, g.persons, g.families, g.locations)
    g.others = Others().read(dir, g.persons, g.families, g.events, g.sources,
                             g.citations, g.locations, g.notes, g.addresses)
    g.citations.resolve(g.persons, g.families, g.events, g.others)
    return g


class BKGenealogy(Genealogy):

    def read(self, dir):
        self.notes = Notes().read(dir)
        self.locations = Locations().read(dir)
        self.sources = Sources().read(dir, self.notes)
        self.citations = Citations().read(dir, self.notes)
        self.persons = Persons().read(dir)
        self.families = Families().read(dir, self.persons)
        self.repositories = {}
        self.addresses = Addresses().read(dir, self.persons, self.families, self.repositories)
        self.events = Events().read(dir, self.persons, self.families, self.locations)
        self.others = Others().read(dir, self.persons, self.families, self.events, self.sources,
                                self.citations, self.locations, self.notes, self.addresses)
        self.citations.resolve(self.persons, self.families, self.events, self.others)
        return self
        