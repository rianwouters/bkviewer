class CheckConsistency:
    @staticmethod
    def exec(session, *args):
        def person_check_none(p, attr):
            l = getattr(p, attr)
            if None in l:
                print(f'{p.fullname} contains empty {l.name}')

        def family_check_none(f, attr):
            l = getattr(f, attr)
            if None in l:
                print(
                    f'{f.partners[0].fullname}x{f.partners[1].fullname} contains empty {l.name}')

        def check_event_witnesses(o, p):
            for e in o.events:
                for w in e.witnesses:
                    if not w:
                        print(f'empty witness in {e.type} event of {p.fullname} (#{p.id})')
                        continue
                    
                    if not w.person:
                        print(f'witness is not linked to a person in {e.type} event of {p.fullname} (#{p.id})')
                        continue

        for p in session.genealogy.persons.values():
            for attr in ['families', 'notes', 'events', 'media', 'images',
                 'names', 'todos', 'citations', 'name_citations', 'child_citations']:
                person_check_none(p, attr)
                check_event_witnesses(p, p)

        for f in session.genealogy.families.values():
            for attr in ['notes', 'events', 'media', 'images', 'citations']:
                family_check_none(f, attr)
                check_event_witnesses(f, f.partners[0])
