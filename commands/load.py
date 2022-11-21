from bk import BKGenealogy


class Load:
    @staticmethod
    def exec(session, *args):
        session.db = args[0] if len(args) else session.db
        session.genealogy = BKGenealogy().read(session.db)
