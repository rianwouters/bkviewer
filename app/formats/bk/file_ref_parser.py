from .field import Field, to_int, to_str
from .parsers import Parser
from models.file_ref import FileRef


class FileRefParser(Parser):
    grammar = [
        Field('space', 4, to_str),
        Field('path', 150, to_str),
        Field('unused1?', 52, to_str),
        Field('unused2?', 3, to_int),
        Field('descr', 100, to_str),
        Field('unused3', 57, to_str),
    ]

    def handle(self, r, n, ref):
        file = FileRef(r['path'], r['descr'])
        ref.files[n-1] = file
        return file
