from formats.bk.msgs_parser import MessageParser

p = MessageParser('C:\\stamboom\\bk\\BKMessg.dt7')
p.read()
p.remove_note(1539)
p.write()