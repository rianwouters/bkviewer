from itertools import accumulate


def _parse(s, grammar):
    pos = accumulate(grammar, lambda t, f: t + f.len, initial=0)
    return {f.name: f.dec_fn(s[n:n+f.len]) for f, n in zip(grammar, pos)}


class Parser():
    def __init__(self, persons, locations, addresses, msgs, todos):
        self.persons = persons
        self.locations = locations
        self.addresses = addresses
        self.msgs = msgs
        self.todos = todos

    def read(self, s, n, ref):
        return self.handle(_parse(s, self.grammar), n, ref)


class FileParser(dict):

    def __init__(self, fname):
        self.fname = fname

    def read(self, *args):
        for r in self.rows():
            self[r['id']] = self.convert(r, *args)
        return self

    def write(self):
        file = open(self.fname, "w")
        try:
            for r in self.values():
                for f in self.grammar:
                    file.write(f.enc_fn(r[f.name]))
                file.write("\n")
        finally:
            file.close()

    # TODO this fails if end of lines or incorrectly mixed up as \x0d \x0d \x0a for example
    # seems to work in most cases but for some reasons sometimes an extra \x0a ends up in some files
    def rows(self):
        with open(self.fname) as f:
            line = f.readline()
            while line:
                bkline = line
                while bkline[-2] != "*":
                    bkline += '\n' + f.readline()
                line = f.readline()
                yield _parse(bkline, self.grammar)
