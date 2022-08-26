class Visitor:
    def __init__(self, action):
        self.action = action

class PedigreeVisitor(Visitor):
    def __init__(self, action):
        super().__init__(action)

    def visit(self, p):
        self.visit_generation(p, 0)

    def visit_generation(self, p, gen):
        if not p:
            return

        for parent_family in p.parents:
            for parent in parent_family.partners:
                self.action.person(parent, p, gen)
                self.visit_generation(parent, gen+1)


class PersonFamilyVisitor(Visitor):
    def __init__(self, action):
        super().__init__(action)

    def visit(self, p):
        self.families(p.families)

    def family(self, f):
        for p in f.partners:
            self.action.person(p)
            self.events(p.events)
        self.action.family(f)
        self.events(f.events)
        self.children(f.children)

    def families(self, families):
        for f in families.values():
            self.family(f)

    def events(self, events):
        for event in events.values():
            self.action.event(event)
            self.witnesses(event.witnesses)

    def witnesses(self, witnesses):
        for w in witnesses.values():
            self.action.witness(w)

    def children(self, children):
        for c in children:
            self.action.person(c)
            self.events(c.events)
