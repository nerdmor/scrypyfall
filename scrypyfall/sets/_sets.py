# standard libraries
from typing import Any
from typing import NewType

# custom libraries
from scrypyfall.foundation import ScrypyfallFoundation
from scrypyfall.foundation import ScrypyfallIterableFoundation
from scrypyfall.foundation import ScrypyfallList

# setting types
SetsTcgplayerId = NewType('SetsTcgplayerId', list)
SetsCode = NewType('SetsCode', ScrypyfallFoundation)
SetsId = NewType('SetsId', ScrypyfallFoundation)


class Sets(ScrypyfallIterableFoundation):
    """General-purpose wrapper for the Sets endpoints.
    
    Wraps the following endpoints: /sets, /sets/:code, /sets/tcgplayer/:id, and
    /sets/:id
    
    
    Attributes:
        tcgplayer (SetsTcgplayer): handler for the TcgPlayer endpoints.
    """
    def __init__(self) -> None:
        """Initializes the object.
        """
        super().__init__('sets')
        # TODO: add header update handling
        self.tcgplayer = SetsTcgplayer()
    
    def __call__(self, **kwargs) -> dict|ScrypyfallList:
        """Allows for the object to be callable, wrapping other methods.
        
        This extends ScrypyfallIterableFoundation, please see kwargs there.
        
        Args:
            code (str, optional): Three to five-letter set code.  If provided,
                wraps self.code(), and ignores id
            id (str, optional): Scryfall ID for the set. If provided, wraps
                self.id()
            

        Returns:
            dict|ScrypyfallList: TODO: fix this
        """
        if 'code' in kwargs:
            # TODO: add other kwargs forwarding
            return self.code(kwargs['code'])
        if 'id' in kwargs:
            # TODO: add other kwargs forwarding
            return self.id(kwargs['id'])
        self.load(**kwargs)
        return self
    
    def code(self, set_code:str) -> dict:
        # TODO: fix this
        return SetsCode(set_code).data
    
    def id(self, id:str) -> dict:
        # TODO: fix this
        return SetsId(id).data


class SetsCode(ScrypyfallFoundation):
    """Wrapper for the /sets/:code endpoint
    """
    def __init__(self, set_code:str) -> None:
        """initializes the object

        Args:
            set_code (str): Three to five-letter set code.

        Raises:
            ValueError: when a provided set code does not match the expected
                pattern
        """
        super().__init__('sets')
        if len(set_code) < 3 or len(set_code) > 5:
            raise ValueError("set_code must be a string with 3 to 5 characters")
        self.data = self.make_request(uri=set_code)


class SetsTcgplayer():
    def __call__(self, id:int) -> dict:
        return self.id(id)

    def id(self, id:int)-> dict:
        return SetsTcgplayerId(id).data


class SetsTcgplayerId(ScrypyfallFoundation):
    def __init__(self, id:int) -> None:
        super().__init__('sets/tcgplayer')
        self.data = self.make_request(uri=str(id))


class SetsId(ScrypyfallFoundation):
    def __init__(self, id:str) -> None:
        super().__init__('sets')
        self.data = self.make_request(uri=id)