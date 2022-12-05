from .field import Field, asterisk, to_boolean, to_int, to_str, modification_dates
from .parsers import FileParser
from models import Source


class SourcesParser(FileParser):
    grammar = [
        Field('id', 8, to_int),
        Field('title', 129, to_str),
        Field('media', 1, to_str),
        Field('abbreviation', 120, to_str),
        Field('author', 120, to_str),
        Field('publisher_year', 120, to_str),
        Field('repo_id', 8, to_int),
        Field('??1', 9, to_str),
        Field('archive_access_number', 80, to_str),
        Field('??', 27, to_str),
        Field('text_id', 9, to_int),
        Field('??', 1, to_str),
        Field('info_id', 9, to_int),
        Field('??2', 1, to_str),
        Field('??3', 61, to_str),
        *modification_dates,
        Field('title_enabled', 1, to_boolean),
        Field('author_enabled', 1, to_boolean),
        Field('publisher_year_enabled', 1, to_boolean),
        Field('abbreviation_enabled', 1, to_boolean),
        Field('print_text', 1, to_boolean),
        Field('print_info', 1, to_boolean),
        Field('parenthesis', 1, to_boolean),
        Field('italics', 1, to_boolean),
        Field('??', 38, to_str),
        Field('next_id', 8, to_int),
        Field('prev_id', 8, to_int),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r, msgs):
        return Source(r['title'], msgs.get_note(r['text_id']), msgs.get_note(r['info_id']))
