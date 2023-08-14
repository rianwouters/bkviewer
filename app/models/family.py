from .array import Array


class Family:
    def __init__(self, partners, children, address=None):
        self.partners = partners
        self.children = children
        self.address = address
        self.notes = Array("Notes")
        self.events = Array("Events")
        self.media = Array("Media")
        self.images = Array("Images")
        self.citations = Array("Citations")

    def __str__(self) -> str:
        fn = map(lambda p: p.fullname if p else "(empty)", self.partners)
        return ' x '.join(fn) + f'{self.events}{self.notes}{self.images}{self.media}{self.citations}'
