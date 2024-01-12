# Standard libraries
from typing import Any
from typing import NewType

# custom libraries
from scrypyfall.foundation import ScrypyfallFoundation
from scrypyfall.foundation import ScrypyfallIterableFoundation
from ..settings import settings

# type definition
Symbology = NewType('Symbology', ScrypyfallIterableFoundation)


class Symbology(ScrypyfallIterableFoundation):
    """Wrapper for the /symbology endpoints
    """
    def __init__(self) -> None:
        """Initialize the object
        """
        # TODO: add header and kwargs forwarding handling
        super().__init__('symbology')
    
    def __call__(self) -> Symbology:
        """Makes the object callable. Loads data and returns self

        Returns:
            Symbology: self
        """
        if settings.lazy_loading is False:
            self.load()
        else:
            self._get_data_page()
        return self
    
    def parse_mana(self, cost:str) -> dict:
        """Wrapper for SymbologyParseMana

        Args:
            cost (str): The mana string to parse.

        Returns:
            dict: the endpoint response
        """
        # TODO: add header and kwargs forwarding handling
        return SymbologyParseMana(cost).data
    
    def parsemana(self, cost:str) -> dict:
        return self.parse_mana(cost)


class SymbologyParseMana(ScrypyfallFoundation):
    """wrapper for the /symbology/parse-mana endpoint.
    """
    def __init__(self, cost:str) -> None:
        """Initializes the object

        Args:
            cost (str): The mana string to parse.
        """
        super().__init__('symbology/parse-mana')
        self.data = self.make_request(params={'cost': cost}, validate_params=False)
