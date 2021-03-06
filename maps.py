from enums import PrivacyType, Sexe, TodoStatus, TodoType, WitnessType, NameType, EventType

privacy_type_map = [
    PrivacyType.CLEAR,
    PrivacyType.NAME_ONLY_DETAILS_BLANK,
    PrivacyType.NAME_ONLY_DETAILS_PRIVATE,
    PrivacyType.ALL_PRIVATE,
    PrivacyType.HIDE_PERSON
]

witness_type_map = dict([
    (0, WitnessType.WITNESS),
    (1, WitnessType.GODPARENT),
    (2, WitnessType.SPONSOR),
    (3, WitnessType.LEGAL_WITNESS),
    (4, WitnessType.INFORMANT),
    (5, WitnessType.PERSON_OF_HONOR),
    (9, WitnessType.OTHER),
])

name_type_map = dict([
    (1, NameType.ALSO_KNOWN_AS),
    (5, NameType.NICK),
    (10, NameType.SHORT),
    (15, NameType.ADOPTED),
    (20, NameType.HEBREW),
    (25, NameType.CENSUS),
    (30, NameType.MARIIED),
    (35, NameType.GERMAN),
    (40, NameType.FARM),
    (45, NameType.BIRTH),
    (50, NameType.INDIAN),
    (55, NameType.FORMAL),
    (60, NameType.CURRENT),
    (65, NameType.SOLDIER),
    (68, NameType.FORMERLY_KNOWN_AS),
    (70, NameType.RELIGIOUS),
    (80, NameType.CALLED),
    (85, NameType.INDIGENOUS),
    (88, NameType.TOMBSTONE),
    (95, NameType.OTHER),
])

event_type_map = dict([
    (1, EventType.BORN),
    (5, EventType.BAPTIZED),
    (9, EventType.CHRISTENED),
    (13, EventType.DIED),
    (16, EventType.BURRIED),
    (19, EventType.CREMATED),
    (23, EventType.ADOPTED_BY_BOTH),
    (30, EventType.ADOPTED_BY_FATHER),
    (40, EventType.ADOPTED_BY_MOTHER),
    (50, EventType.BAPTIZED_LDS),
    (60, EventType.BAR_MITZVAH),
    (70, EventType.BAR_MITZVAH),
    (80, EventType.BLESSING),
    (82, EventType.BRIT_MILAH),
    (85, EventType.CENSUS),
    (90, EventType.CHRISTENED_ADULT),
    (100, EventType.CONFIRMATION),
    (110, EventType.CONFIRMATION_LDS),
    (120, EventType.EMIGRATED),
    (130, EventType.ENDOWMENT_LDS),
    (140, EventType.EVENT),
    (150, EventType.FIRST_COMMUNION),
    (155, EventType.FUNERAL),
    (160, EventType.GRADUATED),
    (170, EventType.IMIGRATED),
    (174, EventType.INTERRED),
    (180, EventType.NATURALIZED),
    (190, EventType.ORDNINATION),
    (200, EventType.PROBATE),
    (210, EventType.RETIREMENT),
    (215, EventType.RESIDED),
    (220, EventType.SEALED_CHILD_LDS),
    (230, EventType.WILL_SIGNED),
    (233, EventType.VARTZEIT),
    (235, EventType.VERIFY_HOME_CHRISTENING),
    (236, EventType.CHURCHING_OF_WOMAN),
    (237, EventType.MEMORIAL_SERVICE),
    (340, None),
    (380, None),
    (381, EventType.NOT_LIVING),
    (385, EventType.NEVER_MARRIED),
    (388, EventType.NO_CHILDREN_FROM_PERSON),
    (399, None),
    (401, EventType.OCCUPATION),
    (405, EventType.MILITARY),
    (410, EventType.RELIGION),
    (420, EventType.EDUCATION),
    (430, EventType.NATIONALITY),
    (440, EventType.CASTE),
    (450, EventType.REF_NUMBER),
    (460, EventType.AFN_NUMER),
    (470, EventType.SOCIAL_SECURITY_NUMBER),
    (480, EventType.PERMANENT_NUMBER),
    (490, EventType.ID_NUMBER),
    (492, EventType.Y_DNA),
    (494, EventType.MT_DNA),
    (496, EventType.AT_DNA),
    (502, EventType.LEGAL_NAME_CHANGE),
    (510, EventType.HEIGHT),
    (520, EventType.WEIGHT),
    (530, EventType.EYE_COLOR),
    (540, EventType.HAIR_COLOR),
    (550, EventType.DESCRIPTION),
    (555, EventType.PROPERTY),
    (560, EventType.MEDICAL_CONDITION),
    (570, EventType.CAUSE_OF_DEATH),
    (580, EventType.NUMBER_OF_CHILDREN_PERSON),
    (590, EventType.ANCESTOR_INTEREST),
    (600, EventType.DESCENDANT_INTEREST),
    (660, None),
    (701, EventType.MARRIED),
    (703, EventType.MARRIED_CIVIL),
    (705, EventType.MARRIED_RELIGIOUS),
    (710, EventType.DIVORCED),
    (720, EventType.MARRIED_BANN),
    (725, EventType.MARRIAGE_BOND),
    (730, EventType.MARRIAGE_CONTRACT),
    (740, EventType.MARRIAGE_LICENSE),
    (750, EventType.MARRIAGE_SETTLEMENT),
    (753, EventType.MARRIAGE_INTENTION),
    (760, EventType.DIVORCE_FILED),
    (770, EventType.SEPARATED),
    (780, EventType.ANULLED),
    (790, EventType.ENGAGED),
    (800, EventType.SEALED_TO_SPOUSE_LDS),
    (805, EventType.RESIDED_FAMILY),
    (810, EventType.EVENT_FAMILY),
    (814, EventType.CENSUS_FAMILY),
    (830, None),
    (860, None),
    (910, EventType.NOT_MARRIED),
    (920, EventType.COMMON_LAW),
    (930, EventType.NO_CHILDREN_FROM_THIS_MARRIAGE),
    (936, None),
    (940, EventType.NUMBER_OF_CHILDREN_FAMILY),
    (960, EventType.MARRIAGE_ID),
    (970, EventType.MARRIAGE_REF),
])

sexe_type_map = dict([
    (0, Sexe.UNKNOWN),
    (1, Sexe.MAN),
    (2, Sexe.WOMAN),
])

todo_type_map = dict([
    (1, TodoType.RESEARCH),
    (2, TodoType.CORRESPONDENCE),
    (9, TodoType.OTHER),
])

todo_status_map = dict([
    (1, TodoStatus.PLAN),
    (2, TodoStatus.STARTED),
    (9, TodoStatus.PROGRESS),
    (9, TodoStatus.COMPLETED),
])
