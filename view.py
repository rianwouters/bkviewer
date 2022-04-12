from enums import EventType
from bk import read


g = read('C:\\stamboom\\bk\\')

p = g.persons[12289]

for f in p.families.values():
    print(' x '.join(map(lambda p: p.fullname, f.partners)))
    for c in f.children:
        print(f'   {c.fullname}')
        for e in c.events.values():
            if e.type.is_baptization():
                for w in e.witnesses.values():
                    print(f'      {w}')


# TODO refactor Collection dicts to arrays the models to get rid of .values()
# TODO refactor collections into models
# TODO add type to functions
# TODO consider parse to add to existing dict iso creating new, needs disjoint dict names in 'others'
# TODO: add addition and modification dates to models
