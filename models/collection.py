class Collection(dict):
    def __init__(self, name):
        self.name = name

    def __str__(self) -> str:
        lines = '\n'.join(str(l) for l in self.values())
        return f'\n{self.name}:\n{lines}\n' if lines else f'\n(No {self.name})'