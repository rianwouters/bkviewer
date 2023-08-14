from .visitor import Visitor


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
