from re import search

class NameSearch:
    @staticmethod
    def exec(session, *args):
        print(f'Matches for {args[0]}')
        s = []
        for p in session.genealogy.person_dict.values():
            for n in p.names:                
                if search(args[0], n.text):
                    s.append(p)
                    break
        s.sort(key=lambda p: p.fullname)
        for p in s:
            print(f'{p.fullname} ({p.id})')
