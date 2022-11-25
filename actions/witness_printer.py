from .action import Action
# from builtins import _

class WitnessPrinter(Action):
    def family(self, f):
        print(' x '.join(map(lambda p: p.fullname, f.partners)))

    def person(self, p):
        # print(f'{p.fullname} #{p.id}')
        pass

    def child(self, p):
        print(f'Child {p.fullname} #{p.id}')

    def event(self, e):
        if len(e.witnesses) > 0:
            print(f'{_(e.type)} {e.date}')

    def witness(self, w):
        print(f'   {w.person.fullname} {_(w.type)} #{w.person.id}')
