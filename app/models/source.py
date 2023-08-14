from .array import Array


class Source:
    def __init__(self, title, text, note, repository):
        self.title = title
        self.text = text
        self.note = note
        self.files = Array('Files')
        self.repository = repository

    def __str__(self) -> str:
        return self.title
