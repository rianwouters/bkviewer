from formats.bk import Genealogy


class Load:
    @staticmethod
    def exec(session, *args):
        session.db = args[0] if len(args) else session.db
        session.genealogy = Genealogy(session.db).read()
