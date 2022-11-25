from .between_dates import BetweenDates
from .from_to_date import FromToDate
from .simple_date import SimpleDate


def create_date(s1, s2, type):
    # date1 = datetime.strptime("%y%m%d", d1) if d1 != '' else None

    if s2 == '':
        return '' if s1 == '' else SimpleDate(s1)

    if type == 1:
        return FromToDate(s1, s2)

    if type == 2:
        return BetweenDates(s1, s2)


def date(row):
    return create_date(row['date1'], row['date2'], row['date_type'])
