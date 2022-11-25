from .visitor import Visitor


class PersonFamilyVisitor(Visitor):
    def __init__(self, action, depth=1):
        super().__init__(action)
        self.depth = depth

    def visit(self, p):
        if self.depth == 0:
            return
        self.depth -= 1
        self.families(p.families)
        self.depth += 1

    def family(self, f):
        self.action.family(f)
        for p in f.partners:
            self.action.person(p)
            self.events(p.events)
        self.events(f.events)
        self.children(f.children)

    def families(self, families):
        for f in families:
            self.family(f)

    def events(self, events):
        for event in events:
            self.action.event(event)
            self.witnesses(event.witnesses)

    def witnesses(self, witnesses):
        for w in witnesses:
            self.action.witness(w)

    def children(self, children):
        for c in children:
            self.action.child(c)
            self.events(c.events)
            self.visit(c)