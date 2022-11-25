from .action import Action


class MissingAncestors(Action):
    def __init__(self, min_gen, max_gen):
        self.min_gen = min_gen
        self.max_gen = max_gen

    def person(self, p, c, gen, *args):
        if not p or p.fullname == 'N.N.':
            if self.min_gen <= gen <= self.max_gen:
                print(
                    f'parent of #{c.id} {c.fullname} missing (generation {gen})')
