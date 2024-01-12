"""Foundation class for Scrypyfall

This "library" contains all the basic objects that will be extended and/or used
in other parts of the module.
"""


# standard libraries
from urllib.parse import urlsplit, parse_qs
from typing import NewType
from typing import Any
from time import sleep
import json

# third-party libraries
import requests

# custom libraries
from .settings import settings

IMAGE_VERSION_OPTIONS = [
    'small',
    'normal',
    'large',
    'png',
    'art_crop',
    'border_crop'
]

ScrypyfallList = NewType('ScrypyfallList', list)
ScrypyfallCollection = NewType('ScrypyfallCollection', list)
ScrypyfallCatalog = NewType('ScrypyfallCatalog', list)


class ScrypyfallException(Exception):
    """Base exception class for the module

    Args:
        error_obj (dict): data to be added to the error, so it can be later
            parsed/documented/raised
    """    
    def __init__(self, error_obj: dict, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_details = {}
        self.error_details.update(error_obj)


class ScrypyfallFoundation():
    """Base class for interacting with Scryfall endpoints.
    
    Attributes:
        url (str): the base url to be used as endpoints are extended.
        data (dict): data that this request/endpoint returned, to be used as
            attributes when using this object as a dict
        headers (dict): headers to be sent with every query. This is in addition
            to whatever is in Settings and is meant to be used for specific
            endpoint needs.
        accepted_params (dict): params that can be sent in a specific endpoint
            call. This makes it easier to make optional parameters for endpoints
            without accepting ANYTHING.
    """
    def __init__(self, _url:str, override_url:bool = False) -> None:
        """Foundation object for endpoints.
        
        Provides a few reusable methods and allows for easier extension.

        Args:
            _url (str): the uri that defines this endpoint. e.g.: 'cards/named'
            override_url (bool, optional): If set to True, _url will be treated 
                as the whole url for the endopoint, and not just the URI.
                Defaults to False.
        """
        if override_url:
            self.url = _url
        else:
            self.url = self._build_base_url(_url)
        
        self.data = None
        
        self.headers = {}
        self.accepted_params = {
            'pretty': {'type': bool}
        }
    
    def __getitem__(self, key:str) -> Any:
        """Allows this to be used as a dict.
        
        Will try to get information from this.data before getting self
        attributes

        Args:
            key (str): name of the attribute to be returned

        Returns:
            Any: The value requested, either from self.data or self.
        """
        if key in self.data:
            return self.data[key]
        return getattr(self, key)

    def _build_base_url(self, _url:str) -> str:
        """Internal method. Builds a URL with protocol and domain defined in
        settings.

        Args:
            _url (str): the uri/page to be accessed

        Returns:
            str: a valid URL
        """        
        return f"{settings.protocol}://{settings.domain}/{_url}"
    
    def _validate_param(self, param:str, value:Any) -> bool:
        """Internal method. Checks if a given parameter is valid for this endpoint.
        
        Validation is made against self.accepted_params.

        Args:
            param (str): name of the parameter to be validated.
            value (Any): value to be validated for the parameter.

        Returns:
            bool: True if {value} is of the correct type for {param}
        """        
        def validate_param_type(value, types):
            if isinstance(types, list):
                for t in types:
                    if isinstance(value, t):
                        return True
                return False
            return isinstance(value, types)

        if param not in self.accepted_params:
            return False
        if not validate_param_type(value, self.accepted_params[param]['type']):
            return False   
        if 'options' in self.accepted_params[param]:
            if value not in self.accepted_params[param]['options']:
                return False
        return True
    
    def _build_url(self, uri:str|None) -> str:
        """Internal method. Builds a callable URL for a given uri.

        Args:
            uri (str | None): the Uri to be called

        Returns:
            str: the full URL built
        """
        if uri is None:
            return self.url
        if uri[0] == '/':
            uri = uri[1:]
        return f"{self.url}/{uri}"
    
    def items(self) -> (Any, Any):
        """Generator method, yielding pairs of key:value for contents of self.data.
        
        This allows for extending classes to be used as dicts

        Yields:
            (Any, Any): Key and values for returned data
        """
        if self.data is None:
            yield None, None
        for k, v in self.data.items():
            yield k, v
    
    def make_request(self, uri:str =None, params: dict =None, headers:dict =None, validate_params:bool =True, overwrite_url:bool =False, method:str ='get', data_payload:dict|str =None, json_payload:dict|str =None) -> dict | ScrypyfallList | ScrypyfallCollection | ScrypyfallCatalog:
        """Makes a request to Scryfall.
        
        This is the main wrapper for actual requests 

        Args:
            uri (str, optional): The URI to be called. If None, will use the
                default URI/URL for the object. Defaults to None.
            params (dict, optional): Any parameters to be sent along with the
                request.
            headers (dict, optional): Any headers to be sent along with the
                request. These will not be saved for furture requests on this
                class.
            validate_params (bool, optional): When False, will skip validating
                parameters. Use when this library is outdated against parameters
                actually available in Scryfall. Defaults to True.
            overwrite_url (bool, optional): If True and a value is provided for
                uri, will skip the URL building and use the provided URI.
                Defaults to False.
            method (str, optional): HTTP method to be used. Defaults to 'get'.
            data_payload (dict | str, optional): when the method is 'post' or
                'put', this payload will be sent with the request in form mode.
            json_payload (dict | str, optional): when the method is 'post' or
                'put', this payload will be sent with the request as a JSON
                payload.

        Raises:
            ValueError: raised when a parameter with a bad value is provided.
            RuntimeError: raised when the response is an invalid JSON.
            ScrypyfallException: raised when the API responds with a non-200
                status code.

        Returns:
            dict | ScrypyfallList | ScrypyfallCollection | ScrypyfallCatalog:
                data in the best way possible for this specific endpoint.
        """
        # preparing request data
        if uri is not None and overwrite_url is True:
            url = uri
        else:
            url = self._build_url(uri)
        if params:
            if validate_params:
                filtered_params = {
                    k:v for k,v
                    in params.items()
                    if self._validate_param(k, v)
                }
            else:
                filtered_params = params
        else:
            filtered_params = None

        # I hate haveing to copy dicts, but this is the only way to safely use this
        combined_headers = settings.headers.copy()
        if self.headers:
            combined_headers.update(self.headers)
        if headers:
            combined_headers.update(headers)

        sleep(settings.sleep_time)
        method = method.lower()
        if method in ['get', 'delete']:
            resp = requests.get(url,
                                headers=combined_headers,
                                params=filtered_params)
        elif method in ['post', 'put']:
            requests_args = {
                'headers': combined_headers,
                'params': filtered_params,
            }
            if data_payload:
                requests_args['data'] = data_payload
            elif json_payload:
                requests_args['json'] = json_payload
            resp = requests.post(url, **requests_args)
        else:
            raise ValueError('Invalid value for method.')

        try:
            jresp = resp.json()
        except requests.exceptions.JSONDecodeError:
            raise RuntimeError(f"response from '{url}' was not a valid JSON")

        if resp.status_code != 200:
            raise ScrypyfallException(jresp, jresp.get('details', 'Error in calling Scryfall API'))

        if jresp['object'] == 'list':
            return ScrypyfallList(jresp)
        elif jresp['object'] == 'collection':
            return ScrypyfallCollection(jresp)
        elif jresp['object'] == 'catalog':
            return ScrypyfallCatalog(jresp)
        return jresp


class ScrypyfallIterableFoundation(ScrypyfallFoundation):
    """Foundation for an interable endpoint.
    
    See ScrypyfallFoundation for several of methods and attributes.
    
    Attributes:
        has_more (bool): indicates wether the last call made with this endpoint
            has more data to return. Specially important when
            settings.lazy_loading is True.
        total (int): the total number of records returned by the last call made
            to this endpoint. Starts as None.
        _iter_index (int): internal. Used to enable iteration on this object as
            if it was a list.
        _next_page_url (str): internal. Used to keep track of what is the next
            url to be called when paginating.
    """
    def __init__(self, _url:str, override_url:bool =False) -> None:
        """Foundation for an interable endpoint.

        Args:
            _url (str): the URL to be used for this enpoint.
            override_url (bool, optional): if True, the provided _url will be
                used instead of a built one. Defaults to False.
        """
        super().__init__(_url, override_url)

        self.accepted_params.update({'page': {'type': int}})

        self.has_more = False
        self.data = []
        self.total = None

        self._iter_index = 0
        self._next_page_url = None
    
    def asdict(self) -> dict:
        """Creates a dict that represents the current state of this endpoint.
        
        This exists mostly so __str__ works properly

        Returns:
            dict: representation of this endpoint as a dict.
        """
        return {
            'has_more': self.has_more,
            'data': self.data,
            'total': self.total
        }

    def __str__(self) -> str:
        """Returns a JSON dump of self.asdict()

        Returns:
            str: a representation of this object as a string
        """
        return json.dumps(self.asdict())

    def __iter__(self):
        self._iter_index = 0
        return self
    
    def __next__(self) -> dict:
        """Allows for usage of this object as an iterative.
        
        This returns an element of this.data, getting the next page if needed.

        Returns:
            dict: an element of this.data
        """
        def _iter_next(self):
            curr_index = self._iter_index
            self._iter_index += 1
            return self.data[curr_index]
        
        if self._iter_index < len(self.data):
            return _iter_next(self)
        
        if self.has_more is True:
            self._get_data_page()
            if self._iter_index < len(self.data):
                return _iter_next(self)

        raise StopIteration

    def __getitem__(self, key:str|int) -> Any:
        """Gets a given element of self.data or an attribute of this object.
        
        An int provided as a key will try to get an element from self.data,
        loading more pages if needed. A str key will return an attribute of the
        object.

        Args:
            key (str | int): the key to be returned

        Raises:
            IndexError: raised when the provided key is an int and is out of
                range.

        Returns:
            Any: the attribute or element requested
        """
        if isinstance(key, int):
            if (key >= len(self.data)
                    and self.has_more is True
                    and self.total is not None
                    and key < self.total):
                while key >= len(self.data):
                    self._get_data_page()

            try:
                return self.data[key]
            except IndexError:
                raise IndexError('index out of range')

        return getattr(self, key)
        
    
    def _get_data_page(self, **kwargs) -> None:
        """Gets the next page of data and loads into self.data.
        
        Args are passed through to the request.
        See ScrypyfallFoundation.make_request() for details.
        """
        if self._next_page_url is None and len(self.data) > 0:
            return

        if self._next_page_url is None:
            params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
            new_data = super().make_request(
                params=params,
                headers=kwargs.get('headers'),
                validate_params=False
            )
        else:
            new_data = super().make_request(
                self._next_page_url,
                headers=kwargs.get('headers'),
                overwrite_url=True,
                validate_params=kwargs.get('validate_params')
            )

        if isinstance(new_data, ScrypyfallList):
            self.data += new_data.data
            self.has_more = new_data.has_more
            self._next_page_url = new_data.next_page_url
            self.total = new_data.total
        elif isinstance(new_data, ScrypyfallCollection):
            self.data += new_data.data
            self.total = new_data.total_values
        elif isinstance(new_data, ScrypyfallCatalog):
            self.data = new_data.data
            self.total = new_data.total_values
        else:
            self.data = [new_data]
            self.has_more = False
        
        if self.total is None and self.has_more is False:
            self.total = len(self.data)
    
    def load(self, **kwargs: Any) -> None:
        """Loads all data at once, iterating through pages. Used when 
        lazy_loading is disabled in settings.
        """
        if self._next_page_url is None and len(self.data) == 0:
            self.has_more = True
        
        while self.has_more:
            self._get_data_page(**kwargs)
        

class IterableResponse():
    """Base class for responses that can be iterated through.
    
    This is meant to be extended by other classes.
    
    Attributes:
        data (list): list of data loaded and handled by this object.
    """
    def __init__(self, data:list) -> None:
        self.data = data
    
    def __iter__(self) -> Any:
        """Allows the class to be used as a iterative object, returning elements
        from self.data.

        Yields:
            Iterator[Any]: elements from self.data
        """
        yield from self.data
    
    def __getitem__(self, key:str|int) -> Any:
        """Allows the classes' attributes to be accessed in a dict-like manner,
        along with the elements in self.data.
        
        If key is an int, will return an element of self.data; otherwise will
        return a property of self.

        Args:
            key (str): attribute/index to be returned.

        Returns:
            Any: value of the requested element.
        """
        if isinstance(key, int):
            return self.data[key]
        return getattr(self, key)
    
    def __str__(self) -> str:
        """Casts self to string (JSON dump of self.asdict())

        Returns:
            str: string representation of self.
        """
        return json.dumps(self.asdict())

    def asdict(self) -> dict:
        """Dummy function to be implemented by classes extending this one.

        Returns:
            dict: an empty dict.
        """
        return {}

    def items(self) -> (Any, Any):
        """Wrapper to allow classes extending this one to be iterated through

        Yields:
            (Any, Any): tuple with a key:value pair from self.asdict().
        """
        for k, v in self.asdict().items():
            yield k, v


class ScrypyfallList(IterableResponse):
    """Represents list objects returned from Scryfall and provides several
    quality-of-life functions.
    
    Please see IterableResponse for most of the methods.
    
    Attributes:
        not_found  (list): List of objects that were not found. Usually as
            part of a search result.
        has_more (bool): True when there are more results than the currently
            loaded.
        total (int): Total amount of records expected in results.
        next_page (int): Number of the next page of results.
        next_page_url (str): URL of the next page of results.
        object (str): Static string representing the kind of object this is.
    """
    def __init__(self, obj:dict) -> None:
        """Initializes the object.

        Args:
            obj (dict): the response from Scryfall that we are trying to parse
                as a list.

        Raises:
            RuntimeError: raised when the given object is not a list.
        """
        if obj.get('object') != 'list':
            raise RuntimeError('Trying to create a list object out of a non-list object')
        super().__init__(obj.get('data', []))

        self.not_found = obj.get('not_found', [])
        self.has_more = obj.get('has_more', False)

        self.total = None
        for k in ['total_cards', 'total']:
            if k in obj:
                self.total = obj[k]
                break
        self.next_page = None
        self.next_page_url = None
        if self.has_more and obj.get('next_page'):
            params = parse_qs(urlsplit(obj['next_page']).query)
            self.next_page = int(params['page'][0])
            self.next_page_url = obj['next_page']
        
        self.object = 'list'
        
    def asdict(self) -> dict:
        """Creates a dictionary representation of self.

        Returns:
            dict: representation of self as a dict.
        """
        return {
            'object': self.object,
            'total': self.total,
            'has_more': self.has_more,
            'next_page': self.next_page,
            'next_page_url': self.next_page_url,
            'data': self.data
        }

    
class ScrypyfallCollection(IterableResponse):
    """Represents a collection object returned from Scryfall and provides
    several quality-of-life functions.
    
    Please see IterableResponse for most of the methods.
    
    Attributes:
        total_values (int): number of elements that this collection should have.
        object (str): Static string representing the kind of object this is.
    """
    def __init__(self, obj:dict) -> None:
        """Initializes the object.

        Args:
            obj (dict): the response from Scryfall that we are trying to parse
                as a list.

        Raises:
            RuntimeError: raised when the provided object is not a collection.
        """
        if obj.get('object') != 'collection':
            raise RuntimeError('Trying to create a collection object out of a non-collection object')
        super().__init__(obj.get('data', []))
        
        self.total_values = obj.get('total_values', 0)
        self.object = 'collection'

    def asdict(self) -> dict:
        """Creates a dict representation of this object.

        Returns:
            dict: object representation of self.
        """
        return {
            'object': self.object,
            'total_values': self.total_values,
            'data': self.data
        }
    

class ScrypyfallCatalog(IterableResponse):
    """Represents a catalog object returned from Scryfall and provides several
    quality-of-life functions.
    
    Please see IterableResponse for most of the methods.
    
    Attributes:
        total_values (int): number of elements that should be in this catalog.
        uri (str): URI of the object being handled.
        object (str): Static string representing the kind of object this is.
    """
    def __init__(self, obj:dict) -> None:
        """Initializes the object.

        Args:
            obj (dict): the response from Scryfall that we are trying to parse
                as a list.

        Raises:
            RuntimeError: raised when the provided object is not a collection.
        """
        if obj.get('object') != 'catalog':
            raise RuntimeError('Trying to create a catalog object out of a non-catalog object')
        super().__init__(obj.get('data', []))
        
        self.total_values = obj.get('total_values', 0)
        self.uri = obj.get('uri')
        self.object = 'catalog'

    def asdict(self) -> dict:
        """Creates a dict representation of this object.

        Returns:
            dict: object representation of self.
        """
        return {
            'object': self.object,
            'uri': self.uri,
            'total_values': self.total_values,
            'data': self.data
        }