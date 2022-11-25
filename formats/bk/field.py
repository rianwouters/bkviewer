from datetime import datetime


class Field:
    def __init__(self, name, len, fn):
        self.name = name
        self.len = len
        self.fn = fn


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


modification_dates = [
    Field('date_added', 8, to_date),
    # 5 means converted from BK5 which did not have this data, so it was converted from the modification date
    Field('date_added_metadata', 4, to_int),
    Field('date_modified', 8, to_date),
    # 5 means converted from BK5 so it may be the same as the added date
    Field('date_modified_metadata', 4, to_int),
]
