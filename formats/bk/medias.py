from .field import Field, to_str
from .files import Files
from .parser import Parser
from models import Media


class Medias(Files):
    def handle(self, r, n, ref):
        media = Media(r['path'], r['descr'])
        ref.media[n-1] = media
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
