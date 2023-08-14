from visitors.actions import BareWitnessReport, WitnessReport
from visitors import TreeVisitor


class Witnesses:
    @staticmethod
    def exec(session, *args):
        bare = args and args[0] == '-b'
        action = BareWitnessReport() if bare else WitnessReport()
        TreeVisitor(action, 1).visit(session.context.families)
        print(action)