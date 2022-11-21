class AsWitness:
    @staticmethod
    def exec(session, *args):
        target = session.context
        for p in session.genealogy.persons.values():
            for e in p.events:
                for w in e.witnesses:
                    if target is w.person:
                        print(
                            f'Witness at: {p.fullname} #{p.id} {e.type} {e.date} {e.loc}')

        for f in session.genealogy.families.values():
            for e in f.events:
                for w in e.witnesses:
                    if target is w.person:
                        p0, p1 = f.partners
                        if not p0:
                            print('p0')
                        if not p1:
                            print('p1')
                        print(
                            f'Witness at: {p0.fullname if p0 else "empty)"} {p0.id  if p0 else ""} & {p1.fullname  if p1 else "(empty)"} {p1.id  if p1 else ""} {e.type} {e.date} {e.loc}')
