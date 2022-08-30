class Action:
    def family(self, f, *args): pass
    def person(self, p, *args): pass
    def child(self, c, *args): pass
    def event(self, e, *args): pass
    def witness(self, w, *args): pass


class MissingAncestors(Action):
    def __init__(self, min_gen, max_gen):
        self.min_gen = min_gen
        self.max_gen = max_gen

    def person(self, p, c, gen, *args):
        if not p or p.fullname == 'N.N.':
            if self.min_gen <= gen <= self.max_gen:
                print(
                    f'parent of #{c.id} {c.fullname} missing (generation {gen})')


class SimpleWitnessPrinter(Action):
    def witness(self, w):
        print(f'{w.person.fullname} #{w.person.id}')


class WitnessPrinter(Action):
    def family(self, f):
        print(' x '.join(map(lambda p: p.fullname, f.partners)))

    def person(self, p):
        print(f'{p.fullname} #{p.id}')

    def event(self, e):
        if len(e.witnesses) > 0:
            print(f'{_(e.type)} {e.date}')

    def witness(self, w):
        print(f'   {w.person.fullname} {_(w.type)} #{w.person.id}')
