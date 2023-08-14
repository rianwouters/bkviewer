from .note import Note


class IntNote(Note):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def __str__(self) -> str:
        return self.text
