from .field import Field, asterisk, to_int, to_str, modification_dates
from .parsers import FileParser
from models import Person, PrivacyType, Sexe


privacy_type_map = [
    PrivacyType.CLEAR,
    PrivacyType.NAME_ONLY_DETAILS_BLANK,
    PrivacyType.NAME_ONLY_DETAILS_PRIVATE,
    PrivacyType.ALL_PRIVATE,
    PrivacyType.HIDE_PERSON
]

sexe_type_map = dict([
    (0, Sexe.UNKNOWN),
    (1, Sexe.MAN),
    (2, Sexe.WOMAN),
])


class PersonsParser(FileParser):

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
        *modification_dates,
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

    def model(self, r):
        return Person(r['id'], sexe_type_map[r['sexe']], r['fullname'], r['firstname'], r['surname'], r['sortingname'], r['title'], privacy_type_map[r['privacy']])
