from enum import Enum

class StrEnum(str, Enum):
    __str__ = str.__str__