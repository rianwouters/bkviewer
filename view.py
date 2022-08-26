from bk import BKGenealogy
from commands import ExitCommand, FamilyCommand, MissingCommand, PersonCommand, WitnessesCommand
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
import gettext

gettext.translation('model', localedir='locale', languages=['nl']).install()

cmd_map = {
    'exit': ExitCommand,
    'person': PersonCommand,
    'family': FamilyCommand,
    'witnesses': WitnessesCommand,
    'missing': MissingCommand,
}


session = PromptSession()
session.genealogy = BKGenealogy().read('C:\\stamboom\\bk\\')

while True:
    try:
        text = session.prompt('> ', completer=WordCompleter(cmd_map.keys), complete_while_typing=True)
        tokens = text.split()

        if len(tokens) == 0:
            continue

        cmd = cmd_map.get(tokens[0])

        if cmd:
            cmd.exec(session, *tokens[1:])
    except:
        pass

# TODO refactor Collection dicts to arrays the models to get rid of .values()
# TODO refactor collections into models
# TODO add type to functions
# TODO consider parse to add to existing dict iso creating new, needs disjoint dict names in 'others'
# TODO: add addition and modification dates to models
