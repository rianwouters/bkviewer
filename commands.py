from actions import MissingAncestors, WitnessPrinter
from visitors import PedigreeVisitor, PersonFamilyVisitor


class ExitCommand: 
    @staticmethod
    def exec():
        exit()

class ExitCommand: 
    @staticmethod
    def exec(session, *args):
        exit()

class PersonCommand:
    @staticmethod
    def exec(session, *args):
        id = int(args[0])
        person = session.genealogy.persons[id]
        session.context = person
        print(f'Context set to person {person.fullname}')

class FamilyCommand:
    @staticmethod
    def exec(session, *args):
        id = int(args[0])
        fam = session.genealogy.families[id]
        session.context = fam
        print(f'Context set to family {fam.partners[0].fullname}, ${fam.partners[1].fullname},')

class WitnessesCommand:
    @staticmethod
    def exec(session, *args):
        PersonFamilyVisitor(WitnessPrinter()).visit(session.context)

class MissingCommand:
    @staticmethod
    def exec(session, *args):
        gen_min = int(args[0])
        gen_max = int(args[1]) if len(args) == 2 else gen_min
        PedigreeVisitor(MissingAncestors(gen_min, gen_max)).visit(session.context)