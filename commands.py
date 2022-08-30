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
        print(
            f'Context set to family {fam.partners[0].fullname}, ${fam.partners[1].fullname},')


class WitnessesCommand:
    @staticmethod
    def exec(session, *args):
        PersonFamilyVisitor(WitnessPrinter()).visit(session.context)


class MissingCommand:
    @staticmethod
    def exec(session, *args):
        gen_min = int(args[0])
        gen_max = int(args[1]) if len(args) == 2 else gen_min
        PedigreeVisitor(MissingAncestors(gen_min, gen_max)
                        ).visit(session.context)


class ChildrenCommand:
    @staticmethod
    def exec(session, *args):
        for f in session.context.families:
            for c in f.children:
                print(c.fullname)


class CheckConsistencyCommand:
    @staticmethod
    def exec(session, *args):
        def person_check_none(p, attr):
            l = getattr(p, attr)
            if None in l:
                print(f'{p.fullname} contains empty {l.name}')

        attrs = ['families', 'notes', 'events', 'media', 'images',
                 'names', 'todos', 'citations', 'name_citations', 'child_citations']
                 
        for p in session.genealogy.persons.values():
            for attr in attrs:
                person_check_none(p, attr)

        def family_check_none(f, attr):
            l = getattr(f, attr)
            if None in l:
                print(f'{f.partners[0].fullname}x{f.partners[1].fullname} contains empty {l.name}')

        attrs = ['notes', 'events', 'media', 'images','citations']

        for f in session.genealogy.families.values():
            for attr in attrs:
                family_check_none(f, attr)
