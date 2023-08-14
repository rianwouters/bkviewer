from models.event_base import EventType
from models.internal_note import IntNote
from re import match, escape

class CheckWitnessNotes:
    @staticmethod
    def exec(session, *args):
        re = r"(?P<type>.*) bij:  (?P<name>.*)  #(?P<id>\d+)( & (?P<name2>.*) #(?P<id2>\d+)|)   (?P<event>\S+(\s\S+)*)(  (?P<date>\S*(\s\S+)*)|)(  (?P<loc>\S+(\s\S+)*)|)(?P<extra>.*)"
        witness_notes = [note for note in session.genealogy.msgs.notes() if match(re, note.text)]
        print(len(witness_notes))
            # else:
            #     if "bij:" in note.text:
            #         print(note.text)
