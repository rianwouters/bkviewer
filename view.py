from audioop import add
from bk import fmt, read, parse, event_name
from models import Address, Citation, Image, Media, Person, Family, IntNote, ExtNote, Location, Source, Event, Fact, Todo, Witness, Name, File
from dates import create_date

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

msg_list = read(dir, 'messages')
messages = {m['id']: m for m in msg_list}


def Note(id):
    s = ''
    while id > 0:
        m = messages[id]
        s, id = s + m['text'], m['next_seq_id']
    return IntNote(s)


loc_list = read(dir, 'locations')
locations = {l['id']: Location(l['name'], l['city'], l['township'], l['county'],
                               l['state_or_province'], l['country'], l['latitude'], l['longitude']) for l in loc_list}

source_list = read(dir, 'sources')
sources = {s['id']: Source(s['title'], Note(
    s['text_id']), Note(s['info_id'])) for s in source_list}

citation_list = list(read(dir, 'citations'))
citations = {c['id']: Citation(c['descr'], Note(
    c['text_id']), Note(c['info_id'])) for c in citation_list}

person_list = read(dir, 'persons')
persons = {p['id']: Person(p['id'], p['fullname'], p['firstname'],
                           p['surname'], p['sortingname'], p['title']) for p in person_list}

families = {}
for r in read(dir, 'marriages'):
    partners = [persons.get(r[p]) for p in ['partner1_id', 'partner2_id']]
    children = [persons[id] for id in r['children']]
    family = Family(partners, children)
    families[r['id']] = family
    for partner, p in zip(partners, ['partner1_seq_nr', 'partner2_seq_nr']):
        if partner:
            partner.families[r[p]] = family

archives = {}
refs = [persons, families, archives]
for a in read(dir, 'mail'):
    id, ref_type = a['ref_id'], a['ref_type']
    refs[ref_type][id] = Address(a['fullname'], a['line1'], a['line2'],
                                 a['line3'], a['line4'], a['phone'], a['fax'], a['email'], a['web'])

events = {}
refs = [persons, families]
for e in read(dir, 'events'):
    if e['ref_id'] > 0:  # skip reuse events
        loc = locations.get(e['loc_id'])
        date = create_date(e['date1'], e['date2'], e['date_type'])
        event = Event(event_name(e['type'], e['custom_name']), date, e['prepos'], loc)
        ref = refs[e['ref_type']][e['ref_id']]
        ref.events[e['seq_nr']] = event
        events[e['id']] = event

others = {}
for o in read(dir, 'others'):
    id = o['id']
    ref_id = o['ref_id']
    n = o['seq_nr']
    t = [o['ref_type'], o['type']]
    if ref_id <= 0:  # skip reuse events
        continue
    refs = [persons, families, others, events, others, events, others, others, [
        others, None, None, None, sources, citations, None, None, None, None][t[1]], locations][t[0]]
    ref = refs[ref_id]
    if t in [[0, 0], [1, 0]]:
        r = parse(o['payload'], fmt['others']['fact'])
        date = create_date(r['date1'], r['date2'], r['date_type'])
        other = Fact(event_name(r['type'], r['custom_name']), date, r['descr'])
        ref.events[n] = other
    elif t in [[0, 1], [1, 1]]:
        r = parse(o['payload'], fmt['others']['name'])
        date = create_date(r['date1'], r['date2'], r['date_type'])
        other = Name(r['type'], r['text'], date)
        ref.names[n] = other
    elif t in [[0, 2], [1, 2], [2, 0], [5, 0], [6, 0], [7, 0], [8, 0], [9, 0]]:
        r = parse(o['payload'], fmt['others']['note'])
        other = Note(r['mess_id']) if r['mess_id'] > 0 else ExtNote(
            r['path'])
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
        date = create_date(r['date1'], r['date2'], r['date_type'])
        loc = locations.get(r['loc_id'])
        arch = archives[r['arch_id']]
        text = Note(r['text_id'])
        other = Todo(r['status'], r['prio'], loc, arch, r['descr'], text)
        ref.todos[n] = other
    elif t in [[3, 0], [4, 0]]:
        r = parse(o['payload'], fmt['others']['witness'])
        person = persons[r['person_id']]
        other = Witness(person, r['role'], r['other role'])
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
    others[id] = other


refs = [persons, families, events, others,
        others, others, others, persons, others, others]
for c in citation_list:
    if c['ref_id'] > 0:
        t = [c['ref_type'], c['type']]
        ref = refs[t[0]][c['ref_id']]
        if t == [7,0]:
            list = ref.child_citations  
        elif t ==[0,1]:
            list = ref.name_citations
        else: 
            list = ref.citations
        list[c['seq_nr']] = citations[c['id']]

print(persons[8])
print(persons[7])
print(families[87])

# TODO: incorporate addition and modificcation dates
# TODO: consider enumeration for message reference types
# TODO: refactor hashing raw lists
# TODO: check bi-directorional reference
#           - source info references
#           - source text references
# TODO add type to functions
# TODO consider parse to add to existing dict iso creating new, needs disjoint dict names in 'others'
# TODO where is the privacy setting stored?
# TODO citation + attachment colors
# TODO citation attachment headings
# TODO citation reach
# TODO refactor date added modified + make str
# TODO consider event name enum 
