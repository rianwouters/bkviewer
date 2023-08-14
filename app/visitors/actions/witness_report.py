from .action import Action
# from builtins import _

class WitnessReport(Action):

    def __init__(self):
        self.report = ''

    def _log(self, s, sep = '\n'):
        self.report += sep + s

    def family(self, f):
        self._log(' x '.join(map(lambda p: p.fullname, f.partners)), sep = '')

    def person(self, p):
        self._log(f'Child {p.fullname} #{p.id}')

    def event(self, e):
        if len(e.witnesses) > 0:
            self._log(f'{_(e.type)} {e.date}')

    def witness(self, w):
        extra_type = f'({w.extra_type})' if w.extra_type else ''
        self._log(f'   {w.person.fullname} {_(w.type)} #{w.person.id} {extra_type}')

    def __str__(self):
        return self.report