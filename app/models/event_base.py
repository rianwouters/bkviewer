from .array import Array
from .str_enum import StrEnum

class EventType(StrEnum):
    BORN = 'Born'
    BAPTIZED = 'Baptized'
    CHRISTENED = 'Christened'
    DIED = 'Died'
    BURRIED = 'Burried'
    CREMATED = 'Cremated'
    ADOPTED_BY_BOTH = 'Adopted by both'
    ADOPTED_BY_FATHER = 'Adopted by father'
    ADOPTED_BY_MOTHER = 'Adopted by mother'
    BAPTIZED_LDS = 'Baptized LDS'
    BAR_MITZVAH = 'Bar Mitzvah'
    BLESSING = 'Blessing'
    BRIT_MILAH = 'Brit Milah'
    CENSUS = 'Census'
    CHRISTENED_ADULT = 'Christened (adult)'
    CONFIRMATION = 'Confirmation'
    CONFIRMATION_LDS = 'Confirmation LDS'
    EMIGRATED = 'Emigrated'
    ENDOWMENT_LDS = 'Endowment LDS'
    EVENT = 'Event'
    FIRST_COMMUNION = 'First Communion'
    FUNERAL = 'Funeral'
    GRADUATED = 'Graduated'
    IMIGRATED = 'Immigrated'
    INTERRED = 'Interred'
    NATURALIZED = 'Naturalized'
    ORDNINATION = 'Ordination'
    PROBATE = 'Probate'
    RETIREMENT = 'Retirement'
    RESIDED = 'Resided'
    SEALED_CHILD_LDS = 'Sealed child LDS'
    WILL_SIGNED = 'Will signed'
    VARTZEIT = 'Yartzeit'
    VERIFY_HOME_CHRISTENING = 'Verify home christening'
    CHURCHING_OF_WOMAN = 'Churching of woman'
    MEMORIAL_SERVICE = 'Memorial serivce'
    NOT_LIVING = 'Not living'
    NEVER_MARRIED = 'Never married'
    NO_CHILDREN_FROM_PERSON = 'No children from this person'
    OCCUPATION = 'Occupation'
    MILITARY = 'Military'
    RELIGION = 'Religion'
    EDUCATION = 'Education'
    NATIONALITY = 'Nationality'
    CASTE = 'Caste'
    REF_NUMBER = 'Ref number'
    AFN_NUMER = 'AFN number'
    SOCIAL_SECURITY_NUMBER = 'Social Security Number'
    PERMANENT_NUMBER = 'Permanent number'
    ID_NUMBER = 'ID number'
    Y_DNA = 'Y-DNA'
    MT_DNA = 'mtDNA'
    AT_DNA = 'atDNA'
    LEGAL_NAME_CHANGE = 'Legal name change'
    HEIGHT = 'Height'
    WEIGHT = 'Weight'
    EYE_COLOR = 'Eye color'
    HAIR_COLOR = 'Hair color'
    DESCRIPTION = 'Description'
    PROPERTY = 'Property'
    MEDICAL_CONDITION = 'Medical condition'
    CAUSE_OF_DEATH = 'Cause of death'
    NUMBER_OF_CHILDREN_PERSON = 'Number of children (person)'
    ANCESTOR_INTEREST = 'Ancestor interest'
    DESCENDANT_INTEREST = 'Descendant interest'
    MARRIED = 'Married'
    MARRIED_CIVIL = 'Married (civil)'
    MARRIED_RELIGIOUS = 'Married (religious)'
    DIVORCED = 'Divorced'
    MARRIED_BANN = 'Married Bann'
    MARRIAGE_BOND = 'Marriage Bond'
    MARRIAGE_CONTRACT = 'Marriage contract'
    MARRIAGE_LICENSE = 'Marriage license'
    MARRIAGE_SETTLEMENT = 'Marriage settlement'
    MARRIAGE_INTENTION = 'Marriage intention'
    DIVORCE_FILED = 'Divorce filed'
    SEPARATED = 'Separated'
    ANULLED = 'Annulled'
    ENGAGED = 'Engaged'
    SEALED_TO_SPOUSE_LDS = 'Sealed to spouse LDS'
    RESIDED_FAMILY = 'Resided (family)'
    EVENT_FAMILY = 'Event (family)'
    CENSUS_FAMILY = 'Census (family)'
    NOT_MARRIED = 'Not married'
    COMMON_LAW = 'Common law'
    NO_CHILDREN_FROM_THIS_MARRIAGE = 'No children from this marriage'
    NUMBER_OF_CHILDREN_FAMILY = 'Number of Children (family)'
    MARRIAGE_ID = 'Marriage ID number'
    MARRIAGE_REF = 'Marriage Reference number'

    def is_baptization(self):
        return self in [
            EventType.BAPTIZED,
            EventType.BAPTIZED_LDS,
            EventType.CHRISTENED,
            EventType.CHRISTENED_ADULT
        ]

    def is_marriage(self):
        return self in [
            EventType.MARRIAGE_BOND,
            EventType.MARRIAGE_CONTRACT,
            EventType.MARRIAGE_INTENTION,
            EventType.MARRIAGE_SETTLEMENT,
            EventType.MARRIED,
            EventType.MARRIED_BANN,
            EventType.MARRIED_CIVIL,
            EventType.MARRIED_RELIGIOUS
        ]

class EventBase:
    def __init__(self, type: EventType, date, ref):
        self.type = type
        self.date = date
        self.notes = Array('Notes')
        self.witnesses = Array("Witnesses")
        self.citations = Array("Citations")
        self.ref = ref
        

    def __str__(self):
        return f'{self.type} {self.date}{self.notes}{self.witnesses}'