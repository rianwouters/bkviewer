from .str_enum import StrEnum


class TodoStatus(StrEnum):
    PLAN = "Plan"
    STARTED = "Started"
    PROGRESS = "Progress"
    COMPLETED = "Completed"


class Todo:
    def __init__(self, date, type, status, prio, loc, arch, descr, text) -> None:
        self.date = date
        self.type = type
        self.status = status
        self.prio = prio
        self.loc = loc
        self.arch = arch
        self.descr = descr
        self.text = text
        self.note = None

    def __str__(self) -> str:
        return f'{self.status} {self.prio} {self.loc} {self.arch} {self.descr} {self.text}'


class TodoType(StrEnum):
    RESEARCH = "Research"
    CORRESPONDENCE = "Correspondence"
    OTHER = "Other"
