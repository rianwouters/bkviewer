from .array import Array


class Source:
    def __init__(self, title, text, note):
        self.title = title
        self.text = text
        self.note = note
        self.files = Array('Files')

    def __str__(self) -> str:
        return self.title
