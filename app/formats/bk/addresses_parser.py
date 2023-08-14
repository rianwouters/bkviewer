from .field import Field, to_int, to_str, modification_dates, asterisk
from .parsers import FileParser
from models import Address, Repository


class AddressesParser(FileParser):
    fname = 'BKMail.dt7'
    grammar = [
        Field('id', 8, to_int),
        Field('ref_type', 1, to_int),
        Field('ref_id', 8, to_int),
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
        *modification_dates,
        Field('unused2?', 16, to_str),
        Field('next_id', 8, to_str),
        Field('prev_id', 8, to_str),
        Field('end_marker', 1, asterisk),
    ]

    def __init__(self, fname, persons, families, repos):
        super().__init__(fname)
        self.persons = persons
        self.families = families
        self.repos = repos

    def model(self, r):
        address = Address(r['fullname'], r['line1'], r['line2'], r['line3'],
                          r['line4'], r['phone'], r['fax'], r['email'], r['web'])
        type, id = r['ref_type'], r['ref_id']

        if type == None:  # skip REUSE lines
            return

        if type == 2:
            id = r['id']
            self.repos[id] = Repository()

        d = [self.persons, self.families, self.repos][type]
        
        # TODO: why is id not an int?
        d[id].address = address

        return address
