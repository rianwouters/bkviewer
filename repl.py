from commands import AsWitness, CheckConsistency, Children, Exit, Experiment, Family, Load, Missing, Person, Witnesses
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from traceback import print_exc
import gettext

gettext.translation('model', localedir='locale', languages=['nl']).install()

cmd_map = {
    'exit': Exit,
    'person': Person,
    'p': Person,
    'family': Family,
    'witnesses': Witnesses,
    'missing': Missing,
    'children': Children,
    'consistency': CheckConsistency,
    'load': Load,
    'aswitness': AsWitness,
    'exp': Experiment
}

session = PromptSession(history=FileHistory('.myhistory'))
session.db = 'C:\\stamboom\\bk\\'
while True:
    try:
        text = session.prompt('> ', completer=WordCompleter(
            cmd_map.keys), complete_while_typing=True)
        cmd_name, *args = text.split()
        cmd_map.get(cmd_name).exec(session, *args)
    except SystemExit:
        exit()
    except Exception as e:
        print_exc()
        print(e)

# TODO option parter in witnesses aktie
# TODO how to split formatting from action results? for example to sort witnesses
# TODO add type to functions
# TODO consider parse to add to existing dict iso creating new, needs disjoint dict names in 'others'
# TODO add addition and modification dates to models
