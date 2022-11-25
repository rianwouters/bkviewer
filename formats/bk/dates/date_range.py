class DateRange:
    def __init__(self, s1, s2):
        self.s = [s1, s2]

    def __str__(self):
        s = list(map(lambda s: 'empty' if s == '' else s, self.s))
        return f'{self.f[0]} {s[0]} {self.f[1]} {s[1]}'
