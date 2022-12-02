from .field import Field, to_str
from .parsers import Parser
from models import Image


class ImageRefParser(Parser):
    grammar = [
        Field('space', 4, to_str),
        Field('path', 150, to_str),
        Field('unused1?', 47, to_str),
        Field('dimensions', 2, to_str),
        Field('unused2?', 3, to_str),
        Field('print_where', 3, to_str),
        Field('descr', 100, to_str),
        Field('unused2?', 57, to_str),
    ]

    def handle(self, r, n, ref):
        image = Image(r['path'], r['descr'], r['dimensions'], r['print_where'])
        ref.images[n-1] = image
        return image
