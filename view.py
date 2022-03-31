from bk import fmt, read, parse
from models import Address, Citation, Image, Media, Person, Family, IntNote, ExtNote, Location, Source, Event, Fact, Todo, Witness, Name, File
from dates import create_date
from maps import event_type_map, name_type_map, privacy_type_map, witness_type_map, sexe_type_map

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


dir = 'C:\\stamboom\\bk\\'


def _date(row):
    return create_date(row['date1'], row['date2'], row['date_type'])


class Handler(dict):
    def __init__(self, *args):
        super().__init__((r['id'], self.process_row(r, *args)) for r in self.rows())

    def rows(self):
        return read(dir, self.grammar)


class Messages(Handler):
    grammar = 'messages'

    def process_row(self, r):
        return r

    def note(self, id):
        s = ''
        while id > 0:
            m = self[id]
            s, id = s + m['text'], m['next_seq_id']
        return IntNote(s.replace('\x12\x13', '\n'))


class Locations(Handler):
    grammar = 'locations'

    def process_row(self, r):
        return Location(r['name'], r['city'], r['township'], r['county'],
                        r['state_or_province'], r['country'], r['latitude'], r['longitude'])


class Sources(Handler):
    grammar = 'sources'

    def process_row(self, r, messages):
        return Source(r['title'], messages.note(r['text_id']), messages.note(r['info_id']))


class Citations(Handler):
    grammar = 'citations'

    def process_row(self, r, messages):
        return Citation(r['descr'], messages.note(r['text_id']), messages.note(r['info_id']))

    def rows(self):
        self.list = super().rows()
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


class Persons(Handler):
    grammar = 'persons'

    def process_row(self, r):
        return Person(r['id'], sexe_type_map[r['sexe']], r['fullname'], r['firstname'], r['surname'], r['sortingname'], r['title'], privacy_type_map[r['privacy']])


class Families(Handler):
    grammar = 'marriages'

    def process_row(self, r):
        partners = [persons.get(r[p]) for p in ['partner1_id', 'partner2_id']]
        children = [persons[id] for id in r['children']]
        family = Family(partners, children)
        for partner, p in zip(partners, ['partner1_seq_nr', 'partner2_seq_nr']):
            if partner:
                partner.families[r[p]] = family
        return family


class Addresses(Handler):
    grammar = 'mail'

    def process_row(self, r,  persons, families):
        address = Address(r['fullname'], r['line1'], r['line2'], r['line3'],
                          r['line4'], r['phone'], r['fax'], r['email'], r['web'])
        # repositories are also added by their reference id
        refs = [persons, families, self]
        id, ref_type = r['ref_id'], r['ref_type']
        refs[ref_type][id] = address
        return address


class Events(Handler):
    grammar = 'events'

    def process_row(self, r,  persons, families):
        refs = [persons, families]
        if r['ref_id'] > 0:  # skip reuse events
            loc = locations.get(r['loc_id'])
            name = r['custom_name']
            event = Event(
                name if name else event_type_map[r['type']], _date(r), r['prepos'], loc)
            ref = refs[r['ref_type']][r['ref_id']]
            ref.events[r['seq_nr']] = event
            return event


class Others(Handler):
    grammar = 'others'

    def process_row(self, o,  persons, families, events, sources, citations, locations, messages):
        ref_id = o['ref_id']
        n = o['seq_nr']
        t = [o['ref_type'], o['type']]
        if ref_id > 0:  # skip reuse events
            refs = [persons, families, self, events, self, events, self, self, [
                self, None, None, None, sources, citations, None, None, None, None][t[1]], locations][t[0]]
            ref = refs[ref_id]
            if t in [[0, 0], [1, 0]]:
                r = parse(o['payload'], fmt['others']['fact'])
                name = r['custom_name']
                other = Fact(
                    name if name else event_type_map[r['type']], _date(r), r['descr'])
                ref.events[n] = other
            elif t in [[0, 1], [1, 1]]:
                r = parse(o['payload'], fmt['others']['name'])
                other = Name(name_type_map[r['type']], r['text'], _date(r))
                ref.names[n] = other
            elif t in [[0, 2], [1, 2], [2, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]:
                r = parse(o['payload'], fmt['others']['note'])
                other = messages.note(
                    r['msg_id']) if r['msg_id'] > 0 else ExtNote(r['path'])
                ref.notes[n] = other
            elif t in [[0, 4], [1, 4]]:
                r = parse(o['payload'], fmt['others']['image'])
                other = Image(r['path'], r['descr'],
                              r['dimensions'], r['print_where'])
                ref.images[n] = other
            elif t in [[0, 7], [1, 7]]:
                r = parse(o['payload'], fmt['others']['file'])
                other = Media(r['path'], r['descr'])
                ref.media[n] = other
            elif t in [[0, 8], [1, 8]]:
                r = parse(o['payload'], fmt['others']['todo'])
                loc = locations.get(r['loc_id'])
                arch = addresses[r['arch_id']]
                text = messages.note(r['text_id'])
                other = Todo(_date(r), r['type'], r['status'], r['prio'],
                             loc, arch, r['descr'], text)
                ref.todos[n] = other
            elif t in [[3, 0], [4, 0]]:
                r = parse(o['payload'], fmt['others']['witness'])
                person = persons[r['person_id']]
                if r['type'] == -1:
                    print(
                        f'WARNING:no explicit witness type defined for person #{r["person_id"]}')
                    r['type'] = 0
                other = Witness(
                    person, witness_type_map[r['type']], r['extra_type'])
                ref.witnesses[n] = other
            elif t in [[8, 4], [8, 5], [9, 4]]:
                r = parse(o['payload'], fmt['others']['file'])
                other = File(r['path'], r['descr'])
                ref.files[n] = other
            elif t in [[9, 9]]:
                r = parse(o['payload'], fmt['others']['location'])
                ref.farm_or_manor_name = r['farm_or_manor_name']
                ref.parish = r['parish']
                ref.postal_address = r['postal_address']
                ref.resident_id = r['resident_id']
                ref.residence_number = r['residence_number']
                ref.farm_number = r['farm_number']
                ref.property_number = r['property_number']
                other = None
            else:
                raise Exception(f"Type combination {t} not implemented")
            return other


messages = Messages()
locations = Locations()
sources = Sources(messages)
citations = Citations(messages)
persons = Persons()
families = Families()
addresses = Addresses(persons, families)
events = Events(persons, families)
others = Others(persons, families, events, sources, citations, locations, messages)
citations.resolve(persons, families, events, others)

print(persons[7])
# TODO move formats into classes
# TODO todo type enumeration
# TODO citation + attachment colors
# TODO: check bi-directorional reference
#           - source info references
#           - source text references
# TODO add type to functions
# TODO consider parse to add to existing dict iso creating new, needs disjoint dict names in 'others'
# TODO consider event name enum
# TODO: add  addition and modification dates to models