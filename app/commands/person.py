class Person:
    @staticmethod
    def exec(session, *args):
        id = int(args[0])
        person = session.genealogy.person_dict[id]
        session.context = person
        print(f'Context set to person {person.fullname}')
