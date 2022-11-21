from commands.as_witness import AsWitness


class Experiment:
    @staticmethod
    def exec(session, *args):
        for p in session.genealogy.persons.values():
            if not p:
                continue

            print(f'{p.fullname} {p.id}')
            session.context = p
            AsWitness.exec(session)
