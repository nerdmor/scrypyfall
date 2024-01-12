# standard libraries
from typing import Any
from typing import NewType

# custom libraries
from scrypyfall.foundation import ScrypyfallFoundation
from scrypyfall.foundation import ScrypyfallIterableFoundation
from scrypyfall.foundation import ScrypyfallList

# setting types
SetsTcgplayerId = NewType('SetsTcgplayerId', dict)
SetsCode = NewType('SetsCode', ScrypyfallFoundation)
SetsId = NewType('SetsId', ScrypyfallFoundation)


class Sets(ScrypyfallIterableFoundation):
    """General-purpose wrapper for the Sets endpoints.
    
    Wraps the following endpoints: /sets, /sets/:code, /sets/tcgplayer/:id, and
    /sets/:id
    
    
    Attributes:
        tcgplayer (SetsTcgplayer): handler for the TcgPlayer endpoints.
    """
    def __init__(self, **kwargs) -> None:
        """Initializes the object.
        
        Args:
            headers (dict, optional): Any headers that should be passed along
                with the requests made.
        """
        super().__init__('sets')
        self.headers.update(kwargs.get('headers', {}))
        self.tcgplayer = SetsTcgplayer()
    
    def __call__(self, **kwargs) -> ScrypyfallList:
        """Returns a given set, based on provided arguments
        Allows for the object to be callable, wrapping other methods.
        This extends ScrypyfallIterableFoundation, please see kwargs there.
        
        Args:
            code (str, optional): Three to five-letter set code.  If provided,
                wraps self.code(), and ignores id and tcgplayer_id
            id (str, optional): Scryfall ID for the set. If provided, wraps
                self.id() and ignores tcgplayer_id
            tcgplayer_id (str, optional): tcgplayer_id or groupId for the set.
                If provided, wraps self.tcgplayer()
            headers (dict, optional): Any headers that should be passed along
                with the requests made.

        Returns:
            ScrypyfallList: Either an intance of SetsCode, SetsId, or
                SetsTcgplayerId, depending on the parameters passed
        """
        if 'code' in kwargs:
            pkwargs = {k:v for k, v in kwargs.items() if k != 'code'}
            return self.code(kwargs['code'], **pkwargs)
        if 'id' in kwargs:
            pkwargs = {k:v for k, v in kwargs.items() if k != 'id'}
            return self.id(kwargs['id'])
        if 'tcgplayer_id' in kwargs:
            pkwargs = {k:v for k, v in kwargs.items() if k != 'tcgplayer_id'}
            return self.tcgplayer(kwargs['tcgplayer_id'], pkwargs)
        self.load(**kwargs)
        return self
    
    def code(self, set_code:str, **kwargs) -> SetsCode:
        """Wrapper for the /sets/:code endpoint.
        
        This instantiates SetsCode. Please see kwargs there.

        Args:
            set_code (str): Three to five-letter set code.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.
        Returns:
            SetsCode: ScrypyfallFoundation-derived object
        """
        kwargs['headers'] = kwargs.get('headers', self.headers)
        return SetsCode(set_code, **kwargs)
    
    def id(self, id:str, **kwargs) -> SetsId:
        """Wrapper for the /sets/:id endpoint

        Args:
            id (str): Scryfall ID for the set.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.

        Returns:
            SetsId: ScrypyfallFoundation-derived object
        """
        kwargs['headers'] = kwargs.get('headers', self.headers)
        return SetsId(id, **kwargs)


class SetsCode(ScrypyfallFoundation):
    """Wrapper for the /sets/:code endpoint
    """
    def __init__(self, set_code:str, **kwargs) -> None:
        """initializes the object
        
        This extends ScrypyfallFoundation. Please see kwargs there.

        Args:
            set_code (str): Three to five-letter set code.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.

        Raises:
            ValueError: when a provided set code does not match the expected
                pattern
        """
        super().__init__('sets')
        if len(set_code) < 3 or len(set_code) > 5:
            raise ValueError("set_code must be a string with 3 to 5 characters")
        self.headers.update(kwargs.get('headers', {}))
        self.data = self.make_request(uri=set_code)


class SetsId(ScrypyfallFoundation):
    """Wrapper for the /sets/:id endpoint
    """
    def __init__(self, id:str, **kwargs) -> None:
        """initializes the object
        
        This extends ScrypyfallFoundation. Please see kwargs there.

        Args:
            id (str): Scryfall ID for the set.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.

        Raises:
            ValueError: when a provided set code does not match the expected
                pattern
        """
        super().__init__('sets')
        self.headers.update(kwargs.get('headers', {}))
        self.data = self.make_request(uri=id)


class SetsTcgplayer():
    """Wrapper to allow SetsTcgplayerId to be instantiated and callable
    """
    def __init__(self, headers:dict =None) -> None:
        """Initializes the object

        Args:
            headers (dict, optional): Any headers that should be passed along
                with the requests made.
        """
        self.headers = headers if headers else {}
    
    def __call__(self, id:int, headers:dict =None) -> SetsTcgplayerId:
        """Instantiates a SetsTcgplayerId, making the calls
        
        This is just an alias for self.id

        Args:
            id (int): tcgplayer_id or groupId for the set.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.

        Returns:
            SetsTcgplayerId: ScrypyfallFoundation-based object
        """
        return self.id(id, headers)

    def id(self, id:int, headers:dict =None) -> SetsTcgplayerId:
        """Instantiates a SetsTcgplayerId, making the calls

        Args:
            id (int): tcgplayer_id or groupId for the set.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.

        Returns:
            SetsTcgplayerId: ScrypyfallFoundation-based object
        """
        self.headers.update(headers if headers else {})
        return SetsTcgplayerId(id, headers=self.headers)


class SetsTcgplayerId(ScrypyfallFoundation):
    """Wraps the /sets/tcgplayer/:id endpoint
    """
    def __init__(self, id:int, **kwargs) -> None:
        """Initializes the object

        Args:
            id (int): tcgplayer_id or groupId for the set.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.
        """
        super().__init__('sets/tcgplayer')
        self.headers.update(kwargs.get('headers', {}))
        self.data = self.make_request(uri=str(id))
