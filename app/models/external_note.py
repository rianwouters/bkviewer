from .note import Note


class ExtNote(Note):
    def __init__(self, path):
        super().__init__()
        self.path = path

    def __str__(self) -> str:
        return self.path
