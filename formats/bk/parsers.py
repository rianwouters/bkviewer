from os.path import join
from itertools import accumulate


def _parse(s, grammar):
    pos = accumulate(grammar, lambda t, f: t + f.len, initial=0)
    return {f.name: f.fn(s[n:n+f.len]) for f, n in zip(grammar, pos)}


class Parser():
    def __init__(self, persons, locations, addresses, notes, todos):
        self.persons = persons
        self.locations = locations
        self.addresses = addresses
        self.notes = notes
        self.todos = todos

    def read(self, s, n, ref):
        return self.handle(_parse(s, self.grammar), n, ref)


class FileParser(dict):

    def read(self, dir, *args):
        for r in self.rows(dir):
            self[r['id']] = self.convert(r, *args)
        return self

    # TODO this fails if end of lines or incorrectly mixed up as \x0d \x0d \x0a for example
    # seems to work in most cases but for some reasons sometimes an extra \x0a ends up in some files
    def rows(self, dir):
        with open(join(dir, self.fname)) as f:
            lines = f.readlines()
        n = 0
        while n < len(lines):
            bkline = lines[n]
            n += 1
            while bkline[-2] != "*":
                bkline += '\n' + lines[n]
                n += 1
            yield _parse(bkline, self.grammar)
