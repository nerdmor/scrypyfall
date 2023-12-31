from typing import Any
from typing import NewType

from scrypyfall.foundation import ScrypyfallFoundation
from scrypyfall.foundation import ScrypyfallIterableFoundation
from scrypyfall.foundation import ScrypyfallList


SetsTcgplayerId = NewType('SetsTcgplayerId', list)
SetsCode = NewType('SetsCode', ScrypyfallFoundation)
SetsId = NewType('SetsId', ScrypyfallFoundation)


class Sets(ScrypyfallIterableFoundation):
    def __init__(self) -> None:
        super().__init__('sets')
        self.tcgplayer = SetsTcgplayer()
    
    def __call__(self, **kwargs) -> dict|ScrypyfallList:
        if 'code' in kwargs:
            return self.code(kwargs['code'])
        if 'id' in kwargs:
            return self.id(kwargs['id'])
        self.load(**kwargs)
        return self
    
    def code(self, set_code) -> SetsCode:
        return SetsCode(set_code).data
    
    def id(self, id) -> SetsId:
        return SetsId(id).data


class SetsCode(ScrypyfallFoundation):
    def __init__(self, set_code:str) -> None:
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

    
        


