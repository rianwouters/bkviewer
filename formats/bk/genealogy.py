from .addresses_parser import AddressesParser
from .citations_parser import CitationsParser
from .events_parser import EventsParser
from .families_parser import FamiliesParser
from .locations_parser import LocationsParser
from .notes_parser import MessageParser
from .others_parser import OthersParser
from .persons_parser import PersonsParser
from .sources_parser import SourcesParser
from models import AbstractGenealogy


class Genealogy(AbstractGenealogy):
    
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
    def read(self, dir):
        self.notes = MessageParser().read(dir)
        self.locations = LocationsParser().read(dir)
        self.sources = SourcesParser().read(dir, self.notes)
        self.citations = CitationsParser().read(dir, self.notes)
        self.persons = PersonsParser().read(dir)
        self.families = FamiliesParser().read(dir, self.persons)
        self.repositories = {}
        self.todos = {}
        self.addresses = AddressesParser().read(
            dir, self.persons, self.families, self.repositories)
        self.events = EventsParser().read(dir, self.persons, self.families, self.locations)
        self.others = OthersParser().read(dir, self.persons, self.families, self.events, self.sources,
                                    self.citations, self.locations, self.notes, self.addresses, self.todos)
        self.citations.resolve(
            self.persons, self.families, self.events, self.others)
        return self
