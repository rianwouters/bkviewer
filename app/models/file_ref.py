class FileRef:
    def __init__(self, path, descr) -> None:
        self.path = path
        self.descr = descr

    def __str__(self) -> str:
        return f'{self.path} {self.descr}'
