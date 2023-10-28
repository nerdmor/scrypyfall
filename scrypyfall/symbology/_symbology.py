from typing import Any
from typing import NewType

from scrypyfall.foundation import ScrypyfallFoundation
from scrypyfall.foundation import ScrypyfallIterableFoundation

Symbology = NewType('Symbology', ScrypyfallIterableFoundation)

class Symbology(ScrypyfallIterableFoundation):
    def __init__(self) -> None:
        super().__init__('symbology')
    
    def __call__(self) -> Symbology:
        self._get_data_page()
        return self
    
    def parse_mana(self, cost:str) -> dict:
        return SymbologyParseMana(cost).data
    
    def parsemana(self, cost:str) -> dict:
        return self.parse_mana(cost)


class SymbologyParseMana(ScrypyfallFoundation):
    def __init__(self, cost:str) -> None:
        super().__init__('symbology/parse-mana')
        self.data = self.make_request(params={'cost': cost}, validate_params=False)
