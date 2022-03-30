#  TODO try to format dates for example with datetime.strptime("%y%m%d", s)

class SimpleDate:
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return '' if self.s == None else self.s


class DateRange:
    def __init__(self, s1, s2):
        self.s = [s1, s2]

    def __str__(self):
        s = list(map(lambda s: 'empty' if s == '' else s, self.s))
        return f'{self.f[0]} {s[0]} {self.f[1]} {s[1]}'


class FromToDate(DateRange):
    f = ['from', 'to']


class BetweenDates(DateRange):
    f = ['between', 'and']


def create_date(s1, s2, type):
    # date1 = datetime.strptime("%y%m%d", d1) if d1 != '' else None

    if s2 == '':
        return '' if s1 == '' else SimpleDate(s1)

    if type == 1:
        return FromToDate(s1, s2)

    if type == 2:
        return BetweenDates(s1, s2)
