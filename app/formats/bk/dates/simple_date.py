#  TODO try to format dates for example with datetime.strptime("%y%m%d", s)

class SimpleDate:
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return '' if self.s == None else self.s
