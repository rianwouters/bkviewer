from visitors.actions import MissingAncestors
from visitors import PedigreeVisitor


class Missing:
    @staticmethod
    def exec(session, *args):
        gen_min = int(args[0])
        gen_max = int(args[1]) if len(args) == 2 else gen_min
        PedigreeVisitor(MissingAncestors(gen_min, gen_max)
                        ).visit(session.context)
