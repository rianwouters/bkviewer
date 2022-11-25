from .addresses import Addresses
from .citations import Citations
from .events import Events
from .families import Families
from .locations import Locations
from .notes import Notes
from .others import Others
from .persons import Persons
from .sources import Sources
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
        self.notes = Notes().read(dir)
        self.locations = Locations().read(dir)
        self.sources = Sources().read(dir, self.notes)
        self.citations = Citations().read(dir, self.notes)
        self.persons = Persons().read(dir)
        self.families = Families().read(dir, self.persons)
        self.repositories = {}
        self.todos = {}
        self.addresses = Addresses().read(
            dir, self.persons, self.families, self.repositories)
        self.events = Events().read(dir, self.persons, self.families, self.locations)
        self.others = Others().read(dir, self.persons, self.families, self.events, self.sources,
                                    self.citations, self.locations, self.notes, self.addresses, self.todos)
        self.citations.resolve(
            self.persons, self.families, self.events, self.others)
        return self
