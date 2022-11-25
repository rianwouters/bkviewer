from .array import Array
from .file import File


class Media(File):
    def __init__(self, path, descr) -> None:
        super().__init__(path, descr)
        self.notes = Array('Notes')
        self.citations = Array('Citations')

    def __str__(self) -> str:
        return f'{super().__str__()}{self.notes}'
