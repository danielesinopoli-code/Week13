from dataclasses import dataclass
from flight_delays.model.airport import Airport

@dataclass
class Connessione: # ORM
    aPartenza : Airport
    aArrivo : Airport
    voli : int