class Array(list):

    def __init__(self, name):
        self.name = name

    def _ensure_length(self, n):
        l = len(self)
        if n > l:
            self.extend([None]*(n - l))

    def __setitem__(self, n, val):
        self._ensure_length(n + 1)
        list.__setitem__(self, n, val)

    def __str__(self) -> str:
        lines = '\n'.join(str(l) for l in self)
        return f'\n{self.name}:\n{lines}\n' if lines else f'\n(No {self.name})'