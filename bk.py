from itertools import accumulate
from os.path import join
from datetime import datetime

_event_type_names = dict([
    (1, 'Born'),
    (5, 'Baptized'),
    (9, 'Christened'),
    (13, 'Died'),
    (16, 'Burried'),
    (19, 'Cremated'),
    (23, 'Adopted by both'),
    (30, 'Adopted by father'),
    (40, 'Adopted by mother'),
    (50, 'Baptized LDS'),
    (60, 'Bar Mitzvah'),
    (70, 'Bar Mitzvah'),
    (80, 'Blessing'),
    (82, 'Brit Milah'),
    (85, 'Census'),
    (90, 'Christened (adult)'),
    (100, 'Confirmation'),
    (110, 'Confirmation LDS'),
    (120, 'Emigrated'),
    (130, 'Endowment LDS'),
    (140, 'Event'),
    (150, 'First Communion'),
    (155, 'Funeral'),
    (160, 'Graduated'),
    (170, 'Immigrated'),
    (174, 'Interred'),
    (180, 'Naturalized'),
    (190, 'Ordination'),
    (200, 'Probate'),
    (210, 'Retirement'),
    (215, 'Resided'),
    (220, 'Sealed child LDS'),
    (230, 'Will signed'),
    (233, 'Yartzeit'),
    (235, 'Verify home christening'),
    (236, 'Churching of woman'),
    (237, 'Memorial serivce'),
    (340, '----------------'),
    (380, '----------------'),
    (381, 'Not living'),
    (385, 'Never marred'),
    (388, 'No children from this person'),
    (399, '----------------'),
    (401, 'Occupation'),
    (405, 'Military'),
    (410, 'Religion'),
    (420, 'Education'),
    (430, 'Nationality'),
    (440, 'Caste'),
    (450, 'Ref number'),
    (460, 'AFN number'),
    (470, 'Social Security Number'),
    (480, 'Permanent number'),
    (490, 'ID number'),
    (492, 'Y-DNA'),
    (494, 'mtDNA'),
    (496, 'atDNA'),
    (502, 'Legal name change'),
    (510, 'Height'),
    (520, 'Weight'),
    (530, 'Eye color'),
    (540, 'Hair color'),
    (550, 'Description'),
    (555, 'Property'),
    (560, 'Medical condition'),
    (570, 'Cause of death'),
    (580, 'Number of children (person)'),
    (590, 'Ancestor interest'),
    (600, 'Descendant interest'),
    (660, '----------------'),
    (701, 'Married'),
    (703, 'Married (civil)'),
    (705, 'Married (religious)'),
    (710, 'Divorced'),
    (720, 'Married Bann'),
    (725, 'Marriage Bond'),
    (730, 'Marriage contract'),
    (740, 'Marriage license'),
    (750, 'Marriage settlement'),
    (753, 'Marriage intention'),
    (760, 'Divorce filed'),
    (770, 'Separated'),
    (780, 'Annulled'),
    (790, 'Engaged'),
    (800, 'Sealed to spouse LDS'),
    (805, 'Resided (family)'),
    (810, 'Event (family)'),
    (814, 'Census (family)'),
    (830, '----------------'),
    (860, '----------------'),
    (910, 'Not married'),
    (920, 'Common law'),
    (930, 'No children from this marriage'),
    (936, '----------------'),
    (940, 'Number of Children (family)'),
    (960, 'Marr ID number'),
    (970, 'Marr Ref number'),
])


def event_type_name(t, name):
    return name if name else _event_type_names[t]

def parse(s, df):
    pos = accumulate(df, lambda t, f: t + f['l'], initial=0)
    return {f['n']: f['t'](s[n:n+f['l']]) for f, n in zip(df, pos)}

# TODO this fails if end of lines or incorrectly mixed up as \x0d \x0d \x0a for example
# seems to work in most cases but for some reasons sometimes an extra \x0a ends up in some files


def read(dir, name):
    df = fmt[name]
    with open(join(dir, df['fname'])) as f:
        lines = f.readlines()
    n = 0
    while n < len(lines):
        bkline = lines[n]
        n += 1
        while bkline[-2] != "*":
            bkline += '\n' + lines[n]
            n += 1
        p = parse(bkline, df['def'])
        yield p


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
    {'l': 8, 't': to_date, 'n': 'date_added'},
    # 5 means converted from BK5 which did not have this data, so it was converted from the modification date
    {'l': 4, 't': to_int, 'n': 'date_added_metadata'},
    {'l': 8, 't': to_date, 'n': 'date_modified'},
    # 5 means converted from BK5 so it may be the same as the added date
    {'l': 4, 't': to_int, 'n': 'date_modified_metadata'},
]

fmt = {
    'persons': {
        'fname': 'BKPerson.dt7',
        'def': [
            {'l': 8, 't': to_int, 'n': 'id'},
            {'l': 5, 't': to_str, 'n': 'surname_prefix_5caps'},
            {'l': 5, 't': to_str, 'n': 'firstname_prefix_5caps'},
            {'l': 140, 't': to_str, 'n': 'fullname'},
            {'l': 10, 't': to_str, 'n': 'surname_prefix_10caps'},
            {'l': 10, 't': to_str, 'n': 'firstname_prefix_10caps'},
            {'l': 40, 't': to_str, 'n': '??'},
            {'l': 40, 't': to_str, 'n': 'prefix'},
            {'l': 40, 't': to_str, 'n': 'postfix'},
            {'l': 40, 't': to_str, 'n': 'firstname'},
            {'l': 40, 't': to_str, 'n': 'surname'},
            {'l': 40, 't': to_str, 'n': 'sortingname'},
            {'l': 50, 't': to_str, 'n': 'title'},
            {'l': 2, 't': to_int, 'n': 'sexe'},
            {'l': 8, 't': to_int, 'n': 'family_id1?'},
            {'l': 8, 't': to_int, 'n': 'family_id2?'},
            {'l': 8, 't': to_str, 'n': '??'},
            {'l': 8, 't': to_str, 'n': '??'},
            {'l': 1, 't': to_str, 'n': 'parent_types1'},
            {'l': 1, 't': to_str, 'n': 'parent_types2'},
            {'l': 8, 't': to_int, 'n': '??'},
            *_modification_dates,
            {'l': 8, 't': to_str, 'n': 'empty?'},
            {'l': 1, 't': to_int, 'n': 'privacy'},
            {'l': 76, 't': to_str, 'n': 'unclear?'},
            {'l': 10, 't': to_str, 'n': 'groups'},
            {'l': 31, 't': to_str, 'n': '??2'},
            {'l': 12, 't': to_str, 'n': 'find_a_grave'},
            {'l': 8, 't': to_int, 'n': 'i1'},
            {'l': 8, 't': to_int, 'n': 'i2'},
            {'l': 8, 't': to_int, 'n': 'i3'},
            {'l': 8, 't': to_int, 'n': 'i4'},
            {'l': 8, 't': to_int, 'n': 'i5'},
            {'l': 8, 't': to_int, 'n': 'i6'},
            {'l': 8, 't': to_int, 'n': 'i7'},
            {'l': 8, 't': to_int, 'n': 'i8'},
            {'l': 1, 't': asterisk, 'n': 'end_marker'},
        ]
    },
    'marriages': {
        'fname': 'BKMarr.dt7',
        'def': [
            {'l': 8, 't': to_int, 'n': 'id'},
            {'l': 8, 't': to_int, 'n': 'partner1_id'},
            {'l': 3, 't': to_int, 'n': 'partner1_seq_nr'},
            {'l': 8, 't': to_int, 'n': 'partner2_id'},
            {'l': 3, 't': to_int, 'n': 'partner2_seq_nr'},
            {'l': 4, 't': to_str, 'n': 'unused?'},
            {'l': 608, 't': to_ids, 'n': 'children'},
            *_modification_dates,
            {'l': 107, 't': to_str, 'n': '??'},
            {'l': 8, 't': to_int, 'n': 'next_id'},
            {'l': 8, 't': to_int, 'n': 'next2_id'},
            {'l': 8, 't': to_int, 'n': 'prev_id'},
            {'l': 8, 't': to_int, 'n': 'prev2_id'},
            {'l': 1, 't': asterisk, 'n': 'end_marker'},
        ]
    },
    'messages': {
        'fname': 'BKMessg.dt7',
        'def': [
            {'l': 9, 't': to_int, 'n': 'id'},
            {'l': 1, 't': to_str, 'n': 'ref_type'},
            # 0 = person, 1 = family, 3 = source information, 5 = event, ...
            {'l': 9, 't': to_int, 'n': 'ref_id'},
            {'l': 3, 't': to_int, 'n': 'seq_nr'},
            {'l': 9, 't': to_int, 'n': '??1'},
            *_modification_dates,
            {'l': 14, 't': to_int, 'n': '??2'},
            {'l': 9, 't': to_int, 'n': 'next_seq_id'},
            {'l': 9, 't': to_int, 'n': 'next_id'},
            {'l': 9, 't': to_int, 'n': 'prev_id'},
            {'l': 1, 't': asterisk, 'n': 'start_marker'},
            {'l': 1200, 't': to_str, 'n': 'text'},
            {'l': 1, 't': asterisk, 'n': 'end_marker'},
        ]
    },
    'others': {
        'fname': 'BKOther.dt7',
        'def': [
            {'l': 9, 't': to_int, 'n': 'id'},
            {'l': 1, 't': to_int, 'n': 'ref_type'},
            {'l': 9, 't': to_int, 'n': 'ref_id'},
            {'l': 1, 't': to_int, 'n': 'type'},
            {'l': 3, 't': to_int, 'n': 'seq_nr'},
            {'l': 366, 't': lambda s: s, 'n': 'payload'},
            {'l': 9, 't': to_int, 'n': 'next_id'},
            {'l': 9, 't': to_int, 'n': 'prev_id'},
            {'l': 1, 't': asterisk, 'n': 'end_marker'},
        ],
        'witness': [
            {'l': 1, 't': to_int, 'n': 'type'},
            {'l': 8, 't': to_int, 'n': 'person_id'},
            {'l': 200, 't': to_str, 'n': 'unused?'},
            {'l': 100, 't': to_str, 'n': 'extra_type'},
            {'l': 57, 't': to_str, 'n': 'unused2?'},
        ],
        'name': [
            {'l': 3, 't': to_int, 'n': 'type'},
            {'l': 1, 't': to_str, 'n': 'space'},
            {'l': 150, 't': to_str, 'n': 'text'},
            {'l': 20, 't': to_str, 'n': 'date1'},
            {'l': 20, 't': to_str, 'n': 'date2'},
            # 1 = "event started date1 and ended date 2", 2 = "event between date1 and date2", 0 or empty = on date1
            {'l': 1, 't': to_str, 'n': 'date_type'},
            {'l': 11, 't': to_str, 'n': 'unused1?'},
            {'l': 3, 't': to_int, 'n': 'print_where'},
            {'l': 157, 't': to_str, 'n': 'unused2?'},
        ],
        'fact': [
            {'l': 3, 't': to_int, 'n': 'type'},
            {'l': 1, 't': to_str, 'n': 'space'},
            {'l': 150, 't': to_str, 'n': 'descr'},
            {'l': 20, 't': to_str, 'n': 'date1'},
            {'l': 20, 't': to_str, 'n': 'date2'},
            # 1 = "event started date1 and ended date 2", 2 = "event between date1 and date2", 0 or empty = on date1
            {'l': 1, 't': to_str, 'n': 'date_type'},
            {'l': 123, 't': to_str, 'n': 'unused1?'},
            {'l': 18, 't': to_str, 'n': 'custom_name'},
            {'l': 30, 't': to_str, 'n': 'unused2?'},
        ],
        'note': [
            {'l': 206, 't': to_str, 'n': 'path'},
            {'l': 3, 't': to_int, 'n': 'print_where'},
            {'l': 100, 't': to_str, 'n': 'unused1?'},
            {'l': 9, 't': to_int, 'n': 'mess_id'},
            {'l': 48, 't': to_str, 'n': 'unused2?'},
        ],
        'media': [
            {'l': 4, 't': to_str, 'n': 'space'},
            {'l': 150, 't': to_str, 'n': 'path'},
            {'l': 100, 't': to_str, 'n': 'descr'},
            {'l': 112, 't': to_str, 'n': 'unused?'},
        ],
        'file': [
            {'l': 4, 't': to_str, 'n': 'space'},
            {'l': 150, 't': to_str, 'n': 'path'},
            {'l': 52, 't': to_str, 'n': 'unused1?'},
            {'l': 3, 't': to_int, 'n': 'unused2?'},
            {'l': 100, 't': to_str, 'n': 'descr'},
            {'l': 57, 't': to_str, 'n': 'unused3'},
        ],
        'image': [
            {'l': 4, 't': to_str, 'n': 'space'},
            {'l': 150, 't': to_str, 'n': 'path'},
            {'l': 47, 't': to_str, 'n': 'unused1?'},
            {'l': 2, 't': to_str, 'n': 'dimensions'},
            {'l': 3, 't': to_str, 'n': 'unused2?'},
            {'l': 3, 't': to_str, 'n': 'print_where'},
            {'l': 100, 't': to_str, 'n': 'descr'},
            {'l': 57, 't': to_str, 'n': 'unused2?'},
        ],
        'todo': [
            {'l': 3, 't': to_int, 'n': 'unused1?'},
            {'l': 1, 't': to_str, 'n': 'space'},
            {'l': 150, 't': to_str, 'n': 'descr'},
            {'l': 20, 't': to_str, 'n': 'date1'},
            {'l': 20, 't': to_str, 'n': 'date2'},
            # 1 = "event started date1 and ended date 2", 2 = "event between date1 and date2", 0 or empty = on date1
            {'l': 1, 't': to_str, 'n': 'date_type'},
            {'l': 1, 't': to_str, 'n': 'status'},
            {'l': 8, 't': to_str, 'n': 'other_flags?'},
            {'l': 1, 't': to_str, 'n': 'prio'},
            {'l': 4, 't': to_str, 'n': 'other_flags?'},
            {'l': 8, 't': to_int, 'n': 'loc_id'},
            {'l': 8, 't': to_str, 'n': 'arch_id'},
            {'l': 85, 't': to_str, 'n': 'unused2?'},
            {'l': 8, 't': to_int, 'n': 'text_id'},
            {'l': 48, 't': to_str, 'n': 'unused3?'},
        ],
        'location': [
            {'l': 4, 't': to_str, 'n': 'space'},
            {'l': 40, 't': to_str, 'n': 'farm_or_manor_name'},
            {'l': 40, 't': to_str, 'n': 'parish'},
            {'l': 125, 't': to_str, 'n': 'postal_address'},
            {'l': 25, 't': to_str, 'n': 'resident_id'},
            {'l': 25, 't': to_str, 'n': 'residence_number'},
            {'l': 25, 't': to_str, 'n': 'farm_number'},
            {'l': 25, 't': to_str, 'n': 'property_number'},
            {'l': 57, 't': to_str, 'n': 'unused?'},
        ]
    },
    'locations': {
        'fname': 'BKLocate.dt7',
        'def': [
            {'l': 8, 't': to_int, 'n': 'id'},
            {'l': 120, 't': to_str, 'n': 'name'},
            {'l': 41, 't': to_str, 'n': 'short_name'},
            {'l': 40, 't': to_str, 'n': 'city'},
            {'l': 40, 't': to_str, 'n': 'township'},
            {'l': 40, 't': to_str, 'n': 'county'},
            {'l': 40, 't': to_str, 'n': 'state_or_province'},
            {'l': 40, 't': to_str, 'n': 'country'},
            {'l': 8, 't': to_int, 'n': 'ref_id??'},
            {'l': 15, 't': to_str, 'n': 'latitude'},
            {'l': 15, 't': to_str, 'n': 'longitude'},
            {'l': 8, 't': to_int, 'n': 'other_id'},
            {'l': 8, 't': to_int, 'n': 'next_id'},
            {'l': 8, 't': to_int, 'n': 'prev_id'},
            {'l': 1, 't': asterisk, 'n': 'end_marker'},
        ]
    },
    'sources': {
        'fname': 'BKSource.dt7',
        'def': [
            {'l': 8, 't': to_int, 'n': 'id'},
            {'l': 129, 't': to_str, 'n': 'title'},
            {'l': 1, 't': to_str, 'n': 'media'},
            {'l': 120, 't': to_str, 'n': 'abbreviation'},
            {'l': 120, 't': to_str, 'n': 'author'},
            {'l': 120, 't': to_str, 'n': 'publisher_year'},
            {'l': 8, 't': to_int, 'n': 'archive_id'},
            {'l': 9, 't': to_str, 'n': '??1'},
            {'l': 80, 't': to_str, 'n': 'archive_access_number'},
            {'l': 27, 't': to_str, 'n': '??'},
            {'l': 9, 't': to_int, 'n': 'text_id'},
            {'l': 1, 't': to_str, 'n': '??'},
            {'l': 9, 't': to_int, 'n': 'info_id'},
            {'l': 1, 't': to_str, 'n': '??2'},
            {'l': 61, 't': to_str, 'n': '??3'},
            *_modification_dates,
            {'l': 1, 't': to_boolean, 'n': 'title_enabled'},
            {'l': 1, 't': to_boolean, 'n': 'author_enabled'},
            {'l': 1, 't': to_boolean, 'n': 'publisher_year_enabled'},
            {'l': 1, 't': to_boolean, 'n': 'abbreviation_enabled'},
            {'l': 1, 't': to_boolean, 'n': 'print_text'},
            {'l': 1, 't': to_boolean, 'n': 'print_info'},
            {'l': 1, 't': to_boolean, 'n': 'parenthesis'},
            {'l': 1, 't': to_boolean, 'n': 'italics'},
            {'l': 38, 't': to_str, 'n': '??'},
            {'l': 8, 't': to_int, 'n': 'next_id'},
            {'l': 8, 't': to_int, 'n': 'prev_id'},
            {'l': 1, 't': asterisk, 'n': 'end_marker'},
        ]
    },
    'citations': {
        'fname': 'BKSourPT.dt7',
        'def': [
            {'l': 9, 't': to_int, 'n': 'id'},
            {'l': 1, 't': to_int, 'n': 'ref_type'},
            {'l': 9, 't': to_int, 'n': 'ref_id'},
            {'l': 2, 't': to_int, 'n': 'type'},
            {'l': 3, 't': to_int, 'n': 'seq_nr'},
            {'l': 8, 't': to_int, 'n': 'source_id'},
            {'l': 100, 't': to_str, 'n': 'descr'},
            # 3 = date and location, 2 = location only, 1 = date only, empty = unspecified
            {'l': 1, 't': to_int, 'n': 'range'},
            {'l': 50, 't': to_int, 'n': 'unused?'},
            {'l': 9, 't': to_int, 'n': 'text_id'},
            {'l': 1, 't': to_int, 'n': 'unused1?'},
            {'l': 9, 't': to_int, 'n': 'info_id'},
            {'l': 1, 't': to_int, 'n': 'unused2?'},
            {'l': 1, 't': to_int, 'n': 'quality'},
            *_modification_dates,
            {'l': 1, 't': to_boolean, 'n': 'text_enabled'},
            {'l': 1, 't': to_boolean, 'n': 'info_enabled'},
            {'l': 1, 't': to_boolean, 'n': 'descr_enabled'},
            {'l': 27, 't': to_str, 'n': 'unused3?'},
            {'l': 9, 't': to_int, 'n': 'next_id'},
            {'l': 9, 't': to_int, 'n': 'prev_id'},
            {'l': 1, 't': asterisk, 'n': 'end_marker'},
        ]
    },
    'events': {
        'fname': 'BKEvent.dt7',
        'def': [
            {'l': 9, 't': to_int, 'n': 'id'},
            {'l': 1, 't': to_int, 'n': 'ref_type'},
            {'l': 8, 't': to_int, 'n': 'ref_id'},
            # type ref-type-specific sequence number shared with 'other' events
            {'l': 3, 't': to_int, 'n': 'seq_nr'},
            {'l': 3, 't': to_int, 'n': 'type'},
            {'l': 2, 't': to_int, 'n': 'prepos'},
            {'l': 20, 't': to_str, 'n': 'date1'},
            {'l': 20, 't': to_str, 'n': 'date2'},
            {'l': 8, 't': to_int, 'n': 'loc_id'},
            # 1 = "event started date1 and ended date2", 2 = "event between date1 and date2", 0 or empty = on date1
            {'l': 9, 't': to_int, 'n': 'date_type'},
            # seems always empty
            {'l': 30, 't': to_str, 'n': '??1'},
            # for families: partner-specific event sequence number, shared with 'other' events?
            {'l': 3, 't': to_int, 'n': 'partner1_seq_nr'},
            {'l': 3, 't': to_int, 'n': 'partner2_seq_nr'},
            # seems always empty
            {'l': 6, 't': to_str, 'n': '??2'},
            {'l': 18, 't': to_str, 'n': 'custom_name'},
            {'l': 9, 't': to_int, 'n': 'next_id'},
            {'l': 9, 't': to_int, 'n': 'prev_id'},
            {'l': 1, 't': asterisk, 'n': 'end_marker'},
        ]
    },
    'mail': {
        'fname': 'BKMail.dt7',
        'def': [
            {'l': 8, 't': to_int, 'n': 'id'},
            {'l': 1, 't': to_int, 'n': 'ref_type'},
            {'l': 8, 't': to_str, 'n': 'ref_id'},
            {'l': 3, 't': to_str, 'n': 'type'},
            {'l': 30, 't': to_str, 'n': 'cs_surname_firstname'},
            {'l': 60, 't': to_str, 'n': 'fullname'},
            {'l': 60, 't': to_str, 'n': 'line1'},
            {'l': 60, 't': to_str, 'n': 'line2'},
            {'l': 60, 't': to_str, 'n': 'line3'},
            {'l': 60, 't': to_str, 'n': 'line4'},
            {'l': 60, 't': to_str, 'n': 'phone'},
            {'l': 60, 't': to_str, 'n': 'fax'},
            {'l': 60, 't': to_str, 'n': 'email'},
            {'l': 60, 't': to_str, 'n': 'web'},
            {'l': 60, 't': to_str, 'n': 'other'},
            {'l': 1, 't': to_int, 'n': 'holiday_list'},
            {'l': 1, 't': to_int, 'n': 'birthday_list'},
            {'l': 1, 't': to_int, 'n': 'reunion_list'},
            {'l': 1, 't': to_int, 'n': 'newsletter'},
            {'l': 1, 't': to_int, 'n': 'other1_list'},
            {'l': 1, 't': to_int, 'n': 'other2_list'},
            {'l': 1, 't': to_int, 'n': 'other3_list'},
            {'l': 1, 't': to_int, 'n': 'unused'},
            {'l': 1, 't': to_int, 'n': 'unused'},
            {'l': 1, 't': to_int, 'n': 'unused'},
            {'l': 179, 't': to_str, 'n': 'unused1?'},
            *_modification_dates,
            {'l': 16, 't': to_str, 'n': 'unused2?'},
            {'l': 8, 't': to_str, 'n': 'next_id'},
            {'l': 8, 't': to_str, 'n': 'prev_id'},
            {'l': 1, 't': asterisk, 'n': 'end_marker'},
        ]
    }
}
