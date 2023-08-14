class Children:
    @staticmethod
    def exec(session, *args):
        for f in session.context.families:
            for c in f.children:
                print(c.fullname)
