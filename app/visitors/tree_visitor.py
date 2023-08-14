from .actions.action import Action
from .visitor import Visitor

class TreeVisitor(Visitor):
    def __init__(self, action: Action, depth=1):
        super().__init__(action)
        self.depth = depth

    def visit(self, fams):
        if self.depth == 0:
            return
        self.depth -= 1
        self.families(fams)
        self.depth += 1

    def families(self, fams):
        for f in fams:
            self.action.family(f)
            self.events(f.events)
            self.persons(f.children)

    def persons(self, persons):
        for p in persons:
            self.action.person(p)
            self.events(p.events)
            self.visit(p)

    def events(self, events):
        for event in events:
            self.action.event(event)
            self.witnesses(event.witnesses)

    def witnesses(self, witnesses):
        for w in witnesses:
            self.action.witness(w)
