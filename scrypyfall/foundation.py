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
    def __init__(self, error_obj, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_details = {}
        self.error_details.update(error_obj)


class ScrypyfallFoundation():
    def __init__(self, _url: str, override_url:bool = False) -> None:
        """Foundation object for endpoints. Provides a few reusable methods and
        allows for easier extension.

        Args:
            _url (str): the uri that defines this endpoint. e.g.: 'cards/named'
            override_url (bool, optional): If set to True, _url will be treated 
            as the whole url for the endopoint, and not just the URI. Defaults to False.
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
        """Allows this to be used as a dict. Will try to get information from
        this.data before getting self attributes

        Args:
            key (str): name of the attribute to be returned

        Returns:
            Any: The value requested, either from self.data or self.
        """
        if key in self.data:
            return self.data[key]
        return getattr(self, key)

    def _build_base_url(self, _url:str) -> str:
        return f"{settings.protocol}://{settings.domain}/{_url}"
    
    def _validate_param(self, param:str, value:Any) -> bool:
        def validate_param_type(value, types):
            if isinstance(types, list):
                for t in types:
                    if isinstance(value, t):
                        return True
            return isinstance(value, types)

        if param not in self.accepted_params:
            return False
        if validate_param_type(value, self.accepted_params[param]['type']) is False:
            return False   
        if 'options' in self.accepted_params[param]:
            if value not in self.accepted_params[param]['options']:
                return False

        return True
    
    def _build_url(self, uri:str|None) -> str:
        if uri is None:
            return self.url
        if uri[0] == '/':
            uri = uri[1:]
        return f"{self.url}/{uri}"
    
    def items(self) -> (Any, Any):
        if self.data is None:
            return None, None
        for k, v in self.data.items():
            yield k, v
    
    def make_request(self, uri:str = None, params: dict = None, headers:dict = None, validate_params:bool = True, overwrite_url:bool = False, method:str = 'get', data_payload:dict|str = None, json_payload:dict|str = None) -> dict | ScrypyfallList | ScrypyfallCollection | ScrypyfallCatalog:
        # preparing request data
        if uri is not None and overwrite_url is True:
            url = uri
        else:
            url = self._build_url(uri)
        if params:
            if validate_params:
                filtered_params = {k:v for k, v in params.items() if self._validate_param(k, v)}
            else:
                filtered_params = params
        else:
            filtered_params = None

        combined_headers = settings.headers.copy()
        if self.headers:
            combined_headers.update(self.headers)
        if headers:
            combined_headers.update(headers)

        sleep(settings.sleep_time)
        if method == 'get':
            resp = requests.get(url, headers=combined_headers, params=filtered_params)
        elif method == 'post':
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
    def __init__(self, _url: str, override_url: bool = False) -> None:
        super().__init__(_url, override_url)

        self.accepted_params.update({'page': {'type': int}})

        self.has_more = False
        self.data = []
        self.total = None

        self._iter_index = 0
        self._next_page_url = None
    
    def asdict(self):
        return {
            'has_more': self.has_more,
            'data': self.data,
            'total': self.total
        }

    def __str__(self):
        return json.dumps(self.asdict())

    def __iter__(self):
        self._iter_index = 0
        return self
    
    def __next__(self) -> dict:
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

    def __getitem__(self, key:str) -> Any:
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
        if self._next_page_url is None and len(self.data) > 0:
            return

        if self._next_page_url is None:
            params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
            new_data = super().make_request(params=params, headers=kwargs.get('headers'), validate_params=False)
        else:
            new_data = super().make_request(self._next_page_url, headers=kwargs.get('headers'), overwrite_url=True)

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
        if self._next_page_url is None and len(self.data) == 0:
            self.has_more = True
        
        while self.has_more:
            self._get_data_page(**kwargs)
        

class IterableResponse():
    def __init__(self, data:list) -> None:
        self.data = data
    
    def __iter__(self) -> Any:
        yield from self.data
    
    def __getitem__(self, key:str) -> Any:
        if isinstance(key, int):
            return self.data[key]
        return getattr(self, key)
    
    def __str__(self) -> str:
        return json.dumps(self.asdict())

    def asdict(self) -> dict:
        return {}

    def items(self) -> (Any, Any):
        for k, v in self.asdict().items():
            yield k, v


class ScrypyfallList(IterableResponse):
    def __init__(self, obj:dict) -> None:
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
        
    def asdict(self):
        return {
            'object': self.object,
            'total': self.total,
            'has_more': self.has_more,
            'next_page': self.next_page,
            'next_page_url': self.next_page_url,
            'data': self.data
        }

    
class ScrypyfallCollection(IterableResponse):
    def __init__(self, obj:dict) -> None:
        if obj.get('object') != 'collection':
            raise RuntimeError('Trying to create a collection object out of a non-collection object')
        super().__init__(obj.get('data', []))
        
        self.total_values = obj.get('total_values', 0)
        self.object = 'collection'

    def asdict(self):
        return {
            'object': self.object,
            'total_values': self.total_values,
            'data': self.data
        }
    

class ScrypyfallCatalog(IterableResponse):
    def __init__(self, obj:dict) -> None:
        if obj.get('object') != 'catalog':
            raise RuntimeError('Trying to create a catalog object out of a non-catalog object')
        super().__init__(obj.get('data', []))
        
        self.total_values = obj.get('total_values', 0)
        self.uri = obj.get('uri')
        self.object = 'catalog'

    def asdict(self):
        return {
            'object': self.object,
            'uri': self.uri,
            'total_values': self.total_values,
            'data': self.data
        }