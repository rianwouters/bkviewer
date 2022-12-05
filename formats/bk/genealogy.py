from .addresses_parser import AddressesParser
from .citations_parser import CitationsParser
from .events_parser import EventsParser
from .families_parser import FamiliesParser
from .locations_parser import LocationsParser
from .msgs_parser import MessageParser
from .others_parser import OthersParser
from .persons_parser import PersonsParser
from .sources_parser import SourcesParser
from os.path import join
from models import AbstractGenealogy


class Genealogy(AbstractGenealogy):

    def __init__(self, dir):
        self.dir = dir

    # Reading order is determined as follows:
    # - locations has to go before events, others
    # - sources has to go before citations
    # - citations has to go before others
    # - persons have to go before families, adresses, events, others, citations
    # - families has to go before adresses, events, others, citations
    # - addresses have to go before others
    # - events have to go before others, citations
    # - others have to go before citations
    #
    # The only cycle in here is others -> citations -> others
    # A "read as late as possible" strategy leads to the following order:
    #  persons, families, locations, events, sources, citations, addresses, others
    # Citation references will he resolved as a separate step in the end.
    def read(self):
        self.msgs = MessageParser(join(self.dir, 'BKMessg.dt7')).read()
        self.locations = LocationsParser(join(self.dir, 'BKLocate.dt7')).read()
        self.sources = SourcesParser(join(self.dir, 'BKSource.dt7')).read(self.msgs)
        self.citations = CitationsParser(
            join(self.dir, 'BKSourPT.dt7')).read(self.msgs)
        self.persons = PersonsParser(join(self.dir, 'BKPerson.dt7')).read()
        self.families = FamiliesParser(
            join(self.dir, 'BKMarr.dt7')).read(self.persons)
        self.repositories = {}
        self.todos = {}
        self.addresses = AddressesParser(join(self.dir, 'BKMail.dt7')).read(
            self.persons, self.families, self.repositories)
        self.events = EventsParser(join(self.dir, 'BKEvent.dt7')).read(
            self.persons, self.families, self.locations)
        self.others = OthersParser(join(self.dir, 'BKOther.dt7')).read(self.persons, self.families, self.events, self.sources,
                                                                  self.citations, self.locations, self.msgs, self.addresses, self.todos)
        self.citations.resolve(
            self.persons, self.families, self.events, self.others)
        return self
