class Family:
    @staticmethod
    def exec(session, *args):
        id = int(args[0])
        fam = session.genealogy.families[id]
        session.context = {'families': [fam]}
        print(
            f'Context set to family {fam.partners[0].fullname}, ${fam.partners[1].fullname}')
