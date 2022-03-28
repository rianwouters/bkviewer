#  TODO try to format dates for example with datetime.strptime("%y%m%d", s)

class SimpleDate:
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return '' if self.s == None else self.s

class FromToDate:
    def __init__(self, frm, to):
        self.frm = frm
        self.to = to

    def __str__(self):
        return f'from {self.s1} to {self.s2}'

class BetweenDates:
    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
    
    def __str__(self):
        return f'between {self.s1} and {self.s2}'

def create_date(s1, s2, type):
    # date1 = datetime.strptime("%y%m%d", d1) if d1 != '' else None

    if s2 == '':
        return '' if s1 == '' else SimpleDate(s1)

    if type == 1:
        return FromToDate(s1, s2)

    if type == 2:
        return BetweenDates(s1, s2)