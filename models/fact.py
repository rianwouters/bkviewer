from .event_base import EventBase


class Fact(EventBase):
    def __init__(self, type, date, ref, descr):
        super().__init__(type, date, ref)
        self.descr = descr

    def __str__(self):
        return f'{self.type} {self.descr} {self.date}{self.notes}{self.witnesses}'
