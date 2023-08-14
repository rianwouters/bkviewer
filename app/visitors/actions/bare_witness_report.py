from .action import Action


class BareWitnessReport(Action):

    def __init__(self):
        self.witnesses = set()

    def witness(self, w):
        self.witnesses.add(w)

    def __str__(self):
        return '\n'.join([f'{w.person.fullname} #{w.person.id} {w.event.date}' for w in sorted(self.witnesses, key=lambda w: w.person.surname)])
