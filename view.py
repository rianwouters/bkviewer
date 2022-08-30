from bk import BKGenealogy
from commands import CheckConsistencyCommand, ChildrenCommand, ExitCommand, FamilyCommand, MissingCommand, PersonCommand, WitnessesCommand
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
import gettext

gettext.translation('model', localedir='locale', languages=['nl']).install()

cmd_map = {
    'exit': ExitCommand,
    'person': PersonCommand,
    'p': PersonCommand,
    'family': FamilyCommand,
    'witnesses': WitnessesCommand,
    'missing': MissingCommand,
    'children': ChildrenCommand,
    'consistency': CheckConsistencyCommand

}


session = PromptSession()
session.genealogy = BKGenealogy().read('C:\\stamboom\\bk\\')

while True:
    try:
        text = session.prompt('> ', completer=WordCompleter(cmd_map.keys), complete_while_typing=True)
        cmd_name, *args = text.split()

        cmd = cmd_map.get(cmd_name)

        cmd.exec(session, *args)
    except SystemExit:
        exit()
    except Exception as e:
        print(e)

# TODO add type to functions
# TODO consider parse to add to existing dict iso creating new, needs disjoint dict names in 'others'
# TODO: add addition and modification dates to models
