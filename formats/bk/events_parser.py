from .dates.date import date
from .field import Field, asterisk, to_int, to_str
from .parsers import FileParser
from models import Event, EventType

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


class EventsParser(FileParser):
    grammar = [
        Field('id', 9, to_int),
        Field('ref_type', 1, to_int),
        Field('ref_id', 8, to_int),
        # type ref-type-specific sequence number shared with 'other' events
        Field('seq_nr', 3, to_int),
        Field('type', 3, to_int),
        Field('prepos', 2, to_int),
        Field('date1', 20, to_str),
        Field('date2', 20, to_str),
        Field('loc_id', 8, to_int),
        # 1 = "event started date1 and ended date2", 2 = "event between date1 and date2", 0 or empty = on date1
        Field('date_type', 9, to_int),
        # seems always empty
        Field('??1', 30, to_str),
        # for families: partner-specific event sequence number, shared with 'other' events?
        Field('partner1_seq_nr', 3, to_int),
        Field('partner2_seq_nr', 3, to_int),
        # seems always empty
        Field('??2', 6, to_str),
        Field('custom_name', 18, to_str),
        Field('next_id', 9, to_int),
        Field('prev_id', 9, to_int),
        Field('end_marker', 1, asterisk),
    ]

    def convert(self, r, persons, families, locations):
        refs = [persons, families]
        # TODO create function to check reuse
        if r['ref_id'] > 0:  # skip reuse events
            loc = locations.get(r['loc_id'])
            name = r['custom_name']
            # TODO create function to get event type
            ref = refs[r['ref_type']][r['ref_id']]
            event = Event(
                name if name else event_type_map[r['type']], date(r), ref, r['prepos'], loc)
            ref.events[r['seq_nr']-1] = event
            return event
