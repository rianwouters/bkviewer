from datetime import datetime


class Field:
    def __init__(self, name, len, dec_fn, enc_fn=None):
        self.name = name
        self.len = len
        self.dec_fn = dec_fn
        self.enc_fn = enc_fn(len) if enc_fn else None


def to_boolean(s):
    return s == '1'


def to_int(s):
    try:
        return None if s.strip() == '' or s == '\x00' else int(s)
    except:
        return s


def to_str(s):
    return s.strip()

def to_str_raw(s):
    return s

def to_date(s):
    try:
        return datetime.strptime(s, "%Y%m%d")
    except:
        return None


def to_ids(s):
    for n in range(0, len(s), 8):
        id = to_int(s[n:n+8])
        if id == None:
            break
        yield id


def asterisk(s):
    if s == '*':
        return s
    raise Exception(f"Parsing error: {s} (expected '*')")


def to_str_r(l):
    return lambda v: l*" " if v == None else f"{{:>{l}}}".format(v)


def str_to_str_l(l):
    return lambda v: l*" " if v == None else f"{{:<{l}}}".format(v.replace('\n', '\x12\x13'))


def date_to_str(l):
    return lambda v: l*" " if v == None else v.strftime("%Y%m%d")


modification_dates = [
    Field('date_added', 8, to_date, date_to_str),
    # 5 means converted from BK5 which did not have this data, so it was converted from the modification date
    Field('date_added_metadata', 4, to_int, to_str_r),
    Field('date_modified', 8, to_date, date_to_str),
    # 5 means converted from BK5 so it may be the same as the added date
    Field('date_modified_metadata', 4, to_int, to_str_r),
]
