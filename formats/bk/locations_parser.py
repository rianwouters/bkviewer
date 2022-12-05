from .field import Field, asterisk, to_int, to_str
from .parsers import FileParser
from models import Location


class LocationsParser(FileParser):
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
