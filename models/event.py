from .event_base import EventBase


class Event(EventBase):
    def __init__(self, type, date, ref, prepos, loc):
        super().__init__(type, date, ref)
        self.prepos = prepos
        self.loc = loc

    def __str__(self):
        return f'{self.type} {self.loc} {self.date}{self.notes}{self.witnesses}'
