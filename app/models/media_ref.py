from .array import Array
from .file_ref import FileRef


class MediaRef(FileRef):
    def __init__(self, path, descr) -> None:
        super().__init__(path, descr)
        self.notes = Array('Notes')
        self.citations = Array('Citations')

    def __str__(self) -> str:
        return f'{super().__str__()}{self.notes}'
