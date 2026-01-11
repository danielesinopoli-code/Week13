from dataclasses import dataclass
from flight_delays.model.airport import Airport


@dataclass
class Connessione:
    aPartenza:Airport
    aArrivo:Airport
    voli:int