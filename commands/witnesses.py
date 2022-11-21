from actions import SimpleWitnessPrinter, WitnessPrinter
from visitors import PersonFamilyVisitor


class Witnesses:
    @staticmethod
    def exec(session, *args):
        bare = args and args[0] == '-b'
        action = SimpleWitnessPrinter() if bare else WitnessPrinter()
        PersonFamilyVisitor(action, 1).visit(session.context)
