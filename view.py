from enums import EventType
from bk import BKGenealogy


g = BKGenealogy().read('C:\\stamboom\\bk\\')

p = g.persons[4664]

for f in p.families.values():
    print(' x '.join(map(lambda p: p.fullname, f.partners)))
    for e in f.events.values():
        if e.type.is_marriage():    
            for w in e.witnesses.values():
                print(f'      {e.type} {w}')
    for c in f.children:
        # print(f'  {c.fullname}')
        for e in c.events.values():
            if e.type.is_baptization():
                # print(f'    {e.date} {e.type}')                
                for w in e.witnesses.values():
                    print(f'{e.date} {w}')

# TODO refactor Collection dicts to arrays the models to get rid of .values()
# TODO refactor collections into models
# TODO add type to functions
# TODO consider parse to add to existing dict iso creating new, needs disjoint dict names in 'others'
# TODO: add addition and modification dates to models
