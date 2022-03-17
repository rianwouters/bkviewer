from itertools import accumulate
from os.path import join


def parse(s, d):
    return {f['n']: f['t'](s[n:n+f['l']].strip()) for f, n in zip(d, accumulate(d, lambda t, f: t + f['l'], initial=0))}

def read(dir, d):
    with open(join(dir, d['fname'])) as f:
        for l in f.readlines():
            print(parse(l, d['def']))


def to_int(s):
    return -1 if s == "" else int(s)

def to_ids(s):
    n,m = 0,8
    while m <= len(s):
        yield int(s[n:m])
        n,m = m,n+8

def asterisk(s):
    if s == '*':
        return s
    raise Exception("Parsing error: expected '*'")

bkperson = {
    'fname': 'BKPerson.dt7',
    'def': [
        {'l': 8, 't': to_int, 'n': 'id'},
        {'l': 5, 't': str, 'n': 'surname_prefix5'},
        {'l': 5, 't': str, 'n': 'firstname_prefix5'},
        {'l': 140, 't': str, 'n': 'fullname'},
        {'l': 10, 't': str, 'n': 'surname_prefix10'},
        {'l': 10, 't': str, 'n': 'firstname_prefix10'},
        {'l': 40, 't': str, 'n': '??'},
        {'l': 40, 't': str, 'n': 'prefix'},
        {'l': 40, 't': str, 'n': 'postfix'},
        {'l': 40, 't': str, 'n': 'firstname'},
        {'l': 40, 't': str, 'n': 'surname'},
        {'l': 40, 't': str, 'n': 'sortingname'},
        {'l': 50, 't': str, 'n': 'titel'},
        {'l': 2, 't': str, 'n': 'sexe'},
        {'l': 8, 't': to_int, 'n': 'family_id1?'},
        {'l': 8, 't': to_int, 'n': 'family_id2?'},
        {'l': 8, 't': str, 'n': '??'},
        {'l': 8, 't': str, 'n': '??'},
        {'l': 1, 't': str, 'n': 'parent_types1'},
        {'l': 1, 't': str, 'n': 'parent_types2'},
        {'l': 8, 't': to_int, 'n': '??'},
        {'l': 8, 't': to_int, 'n': 'date_added'},
        # 5 means converted from BK5 which did not have this data, so it was converted from the modification date
        {'l': 4, 't': to_int, 'n': 'date_added_metadata'},
        {'l': 8, 't': to_int, 'n': 'date_modified'},
        # 5 means converted from BK5 so it may be the same as the added date
        {'l': 4, 't': to_int, 'n': 'date_modified_metadata'},
        {'l': 85, 't': str, 'n': '??'},
        {'l': 10, 't': str, 'n': 'groups'},
        {'l': 31, 't': str, 'n': '??'},
        {'l': 12, 't': str, 'n': 'find_a_grave'},
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
}

bkmessg = {
    'fname': 'BKMessg.dt7',
    'def': [
        {'l': 9, 't': to_int, 'n': 'id'},
        {'l': 1, 't': str, 'n': 'type'},
        # 0 = person, 1 = family, 3 = source information, ...
        {'l': 9, 't': to_int, 'n': 'ref_id'},
        {'l': 3, 't': to_int, 'n': 'seq_nr'},
        {'l': 9, 't': to_int, 'n': '??'},
        {'l': 8, 't': to_int, 'n': 'date_added'},
        # 5 means converted from BK5 which did not have this data, so it was converted from the modification date
        {'l': 4, 't': to_int, 'n': 'date_added_metadata'},
        {'l': 8, 't': to_int, 'n': 'date_modified'},
        # 5 means converted from BK5 so it may be the same as the added date
        {'l': 4, 't': to_int, 'n': 'date_modified_metadata'},
        {'l': 14, 't': to_int, 'n': '??'},
        {'l': 9, 't': to_int, 'n': 'next_seq_id'},
        {'l': 9, 't': to_int, 'n': 'next_id'},
        {'l': 9, 't': to_int, 'n': 'prev_id'},
        {'l': 1, 't': asterisk, 'n': 'start_marker'},
        {'l': 1200, 't': str, 'n': 'text'},
        {'l': 1, 't': asterisk, 'n': 'end_marker'},
    ]
}

bkmarr = {
    'fname': 'BKMarr.dt7',
    'def': [
        {'l': 8, 't': to_int, 'n': 'id'},
        {'l': 8, 't': to_int, 'n': 'partner1_id'},
        {'l': 3, 't': to_int, 'n': 'partner1_seq_nr'},
        {'l': 8, 't': to_int, 'n': 'partner2_id'},
        {'l': 3, 't': to_int, 'n': 'partner2_seq_nr'},
        {'l': 4, 't': str, 'n': 'unused?'},
        {'l': 608, 't': to_ids, 'n': 'children'},
        {'l': 8, 't': to_int, 'n': 'date_added'},
        # 5 means converted from BK5 which did not have this data, so it was converted from the modification date
        {'l': 4, 't': to_int, 'n': 'date_added_metadata'},
        {'l': 8, 't': to_int, 'n': 'date_modified'},
        # 5 means converted from BK5 so it may be the same as the added date
        {'l': 4, 't': to_int, 'n': 'date_modified_metadata'},
        {'l': 107, 't': str, 'n': '??'},
        {'l': 8, 't': to_int, 'n': 'next_id'},
        {'l': 8, 't': to_int, 'n': 'next2_id'},
        {'l': 8, 't': to_int, 'n': 'prev_id'},
        {'l': 8, 't': to_int, 'n': 'prev2_id'},
        {'l': 1, 't': asterisk, 'n': 'end_marker'},
    ]
}

bkother = {
    'fname': 'BKOther.dt7',
    'def': [
        {'l': 9, 't': to_int, 'n': 'id'},
        {'l': 1, 't': to_int, 'n': 'ref_type'},
        {'l': 9, 't': to_int, 'n': 'ref_id'},
        {'l': 1, 't': to_int, 'n': 'type'},
        {'l': 3, 't': to_int, 'n': 'seq_nr'},
        {'l': 3, 't': to_int, 'n': 'subtype'},
        {'l': 1, 't': str, 'n': 'space'},
        {'l': 150, 't': str, 'n': 'text'},
        {'l': 20, 't': str, 'n': 'date1'},
        {'l': 20, 't': str, 'n': 'date2'},
        {'l': 1, 't': str, 'n': 'dates_type'},
        {'l': 1, 't': str, 'n': 'status'},
        {'l': 8, 't': str, 'n': 'other_flags?'},
        {'l': 1, 't': str, 'n': 'prio'},
        {'l': 4, 't': str, 'n': 'other_flags?'},
        {'l': 8, 't': str, 'n': 'loc_id'},
        {'l': 8, 't': str, 'n': 'arch_id'},
        {'l': 85, 't': str, 'n': '??'},
        {'l': 8, 't': to_int, 'n': 'text_id'},
        {'l': 48, 't': str, 'n': '??'},
        {'l': 9, 't': to_int, 'n': 'next_id'},
        {'l': 9, 't': to_int, 'n': 'prev_id'},
        {'l': 1, 't': asterisk, 'n': 'end_marker'},
    ]
}

bklocate = {
    'fname': 'BKLocate.dt7',
    'def': [
        {'l': 8, 't': to_int, 'n': 'id'},
        {'l': 361, 't': str, 'n': 'text'},
        {'l': 1, 't': to_int, 'n': 'flag'},
        {'l': 45, 't': to_int, 'n': '??'},
        {'l': 8, 't': to_int, 'n': 'next_id'},
        {'l': 8, 't': to_int, 'n': 'prev_id'},
        {'l': 1, 't': asterisk, 'n': 'end_marker'},
    ]
}


read('C:\\stamboom\\bk\\', bklocate)
# read('C:\\stamboom\\bk\\', bkperson)
# read('C:\\stamboom\\bk\\', bkmessg)


# TODO: add filename to definitions
