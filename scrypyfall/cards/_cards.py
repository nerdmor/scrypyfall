from typing import Any
from typing import NewType

from scrypyfall.foundation import ScrypyfallFoundation
from scrypyfall.foundation import ScrypyfallIterableFoundation
from scrypyfall.foundation import ScrypyfallList
from scrypyfall.foundation import IMAGE_VERSION_OPTIONS


CardsSearch = NewType('CardsSearch', list)
CardsNamed = NewType('CardsNamed', list)
CardsAutocomplete = NewType('CardsAutocomplete', dict)
CardsRandom = NewType('CardsRandom', dict)
CardsCollection = NewType('CardsCollection', dict)
CardsCodeNumber = NewType('CardsCodeNumber', dict)
CardsById = NewType('CardsMultiverse', dict)
CardsOracle = NewType('CardsOracle', dict)
CardsRulings = NewType('CardsRulings', list)

class Cards:
    def __init__(self) -> None:
        self.multiverse = CardsById('multiverse')
        self.mtgo = CardsById('mtgo')
        self.arena = CardsById('arena')
        self.tcgplayer = CardsById('tcgplayer')
        self.cardmarket = CardsById('cardmarket')
        self._scryfall = CardsById('scryfall')

    def __call__(self, id:str, **kwargs: Any) -> CardsById:
        return self._scryfall(id, **kwargs)

    def search(self, q:str, **kwargs: Any) -> CardsSearch:
        return CardsSearch(q, **kwargs)
    
    def named(self, **kwargs: Any) -> CardsNamed:
        return CardsNamed(**kwargs)[0]
    
    def autocomplete(self, q:str, **kwargs: Any) -> CardsAutocomplete:
        return CardsAutocomplete(q, **kwargs).data
    
    def random(self, **kwargs: Any) -> CardsRandom:
        return CardsRandom(**kwargs).data
    
    def collection(self, identifiers:list, **kwargs: Any) -> CardsCollection:
        return CardsCollection(identifiers, **kwargs)
    
    def code(self, code:str, number:str = None, lang:str = None, **kwargs:Any) -> CardsCodeNumber:
        return CardsCodeNumber(code, number=number, lang=lang, **kwargs)
    
    def oracle(self, id:str, **kwargs:Any) -> None:
        return CardsOracle(id, **kwargs).data
    


class CardsSearch(ScrypyfallIterableFoundation):
    def __init__(self, q:str|dict, **kwargs: Any) -> None:
        super().__init__('cards/search')
        self.accepted_params.update({
            'q': {'type': str},
            'unique': {'type': str, 'options': ['cards', 'art', 'print']},
            'order': {'type': str, 'options': ['name', 'set', 'released', 'rarity', 'color', 'usd', 'tix', 'eur', 'cmc', 'power', 'toughness', 'edhrec', 'penny', 'artist', 'review']},
            'dir': {'type': str, 'options': ['auto', 'asc', 'desc']},
            'include_extras': {'type': bool},
            'include_multilingual': {'type': bool},
            'include_variations': {'type': bool},
            'format': {'type': str, 'options': ['json', 'csv']}
        })
        
        if 'headers' in kwargs:
            self.headers.update(kwargs['headers'])
        
        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        params['q'] = q
        self._get_data_page(validate_params=False, **params)


class CardsNamed(ScrypyfallIterableFoundation):
    def __init__(self, **kwargs) -> None:
        super().__init__('cards/named')
        self.accepted_params.update({
            'exact': {'type': str},
            'fuzzy': {'type': str},
            'set': {'type': str},
            'format': {'type': str, 'options': ['json', 'text', 'image']},
            'face': {'type': str},
            'version': {'type': str, 'options': IMAGE_VERSION_OPTIONS}
        })

        if 'exact' not in kwargs and 'fuzzy' not in kwargs:
            raise ValueError("Either 'exact' or 'fuzzy' parameters must be provided")
        if 'exact' in kwargs and 'fuzzy' in kwargs:
            raise ValueError("Either 'exact' or 'fuzzy' parameters must be provided, but not both")

        if 'headers' in kwargs:
            self.headers.update(kwargs['headers'])
        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        self._get_data_page(validate_params=False, **params)
        

class CardsAutocomplete(ScrypyfallFoundation):
    def __init__(self, q:str, **kwargs: Any) -> None:
        super().__init__('cards/autocomplete')
        self.accepted_params.update({
            'q': {'type': str},
            'include_extras': {'type': bool}
        })

        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        params['q'] = q
        self.data = self.make_request(params=params, validate_params=False, headers=kwargs.get('headers'))


class CardsRandom(ScrypyfallFoundation):
    def __init__(self, **kwargs: Any) -> None:
        super().__init__('cards/random')
        self.accepted_params.update({
            'q': {'type': str},
            'format': {'type': str, 'options': ['json', 'text', 'image']},
            'face': {'type': str},
            'version': {'type': str, 'options': IMAGE_VERSION_OPTIONS}
        })

        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        if not params:
            params = None
        self.data = self.make_request(validate_params=False, params=params, headers=kwargs.get('headers'))
    

class CardsCollection(ScrypyfallIterableFoundation):
    def __init__(self, identifiers:list, **kwargs: Any) -> None:
        super().__init__('cards/collection')

        if not identifiers:
            raise ValueError("A non-empty list of identifiers is needed")

        if len(identifiers) > 75:
            raise ValueError(f"A maximum of 75 identifiers are allowed. {len(identifiers)} provided.")

        allowed_keys = {
            'id': str,
            'mtgo_id': int,
            'multiverse_id': int,
            'oracle_id': str,
            'illustration_id': str,
            'name': str,
            'collector_number': str,
            'set': str
        }

        for ide in identifiers:
            if not isinstance(ide, dict):
                raise ValueError('All elements in an identifier array must be dicts')
            for k, v in ide.items():
                if v is None:
                    raise ValueError(f"Null identifiers are not allowed")
                if k not in allowed_keys:
                    raise ValueError(f"Invalid identifier '{k}' in list")
                if not isinstance(v, allowed_keys[k]):
                    raise ValueError(f"Values of identifiers '{k}' must be {allowed_keys[k]}, {type(v)} provided")
                if k == 'set' and 'name' not in ide and 'collector_number' not in ide:
                    raise ValueError("'set' identifiers must always have a collector number or name in the same request")
        
        if 'headers' in kwargs:
            self.headers.update(kwargs['headers'])
        
        self.has_more = False
        self.not_found = []

        self._get_data_page(payload={'identifiers': identifiers}, **kwargs)
    
    def asdict(self):
        return {
            'has_more': self.has_more,
            'data': self.data,
            'total': self.total,
            'not_found': self.not_found
        }
        
    def _get_data_page(self, **kwargs) -> None:
        if self.data or self.not_found:
            return
        if 'payload' not in kwargs:
            raise ValueError('payload is mandatory')

        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        new_data = super().make_request(params=params, validate_params=False, method='post', json_payload=kwargs['payload'])
        if isinstance(new_data, ScrypyfallList):
            self.data += new_data.data
            self.total = len(self.data)
            self.not_found = new_data.not_found
        else:
            raise ValueError('invalid response from Scryfall. Could not process response as a list')
    
        
class CardsCodeNumber(ScrypyfallFoundation):
    def __init__(self, code:str, **kwargs:Any) -> None:
        super().__init__(f'cards/{code}')

        self.accepted_params.update({
            'format': {'type': str, 'options': ['json', 'text', 'image']},
            'face': {'type': str},
            'version': {'type': str, 'options': IMAGE_VERSION_OPTIONS}
        })
        self.code = code
        self.num = kwargs.get('number', None)
        self.lan = kwargs.get('lang', None)

        if self.num:
            self._request_wrapper(**kwargs)

    
    def _request_wrapper(self, **kwargs:Any) -> None:
        if self.lan is None:
            self.url = self._build_base_url(f'cards/{self.code}/{self.num}')
        else:
            self.url = self._build_base_url(f'cards/{self.code}/{self.num}/{self.lan}')
        
        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        if not params:
            params = None
        self.data = self.make_request(validate_params=False, params=params)

    
    def number(self, number:int|str, **kwargs:Any) -> CardsCodeNumber:
        self.num = str(number)
        self._request_wrapper(**kwargs)
        return self

    def lang(self, lang:str, **kwargs:Any) -> CardsCodeNumber:
        self.lan = lang
        self._request_wrapper(**kwargs)
        return self
    
    def rulings(self, **kwargs: Any) -> CardsRulings:
        return CardsRulings('code', code=self.code, number=self.num, **kwargs)


class CardsById(ScrypyfallFoundation):
    def __init__(self, id_type:str, **kwargs:Any) -> None:
        allowed_id_types = ['multiverse', 'mtgo', 'arena', 'tcgplayer', 'cardmarket', 'scryfall']
        if id_type not in allowed_id_types:
            raise ValueError(f"invalid id type: {id}")
        
        if id_type == 'scryfall':
            _url = 'cards'
        else:
            _url = f'cards/{id_type}'
        super().__init__(_url)

        self.accepted_params.update({
            'format': {'type': str, 'options': ['json', 'text', 'image']},
            'face': {'type': str},
            'version': {'type': str, 'options': IMAGE_VERSION_OPTIONS}
        })

        self.id = None
        self.id_type = id_type
    
    def __call__(self, id:int|str, **kwargs) -> CardsById:
        self.id = str(id)
        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        if not params:
            params = None
        self.data = self.make_request(self.id, params=params, headers=kwargs.get('headers'), validate_params=False)
        return self
    
    def rulings(self, **kwargs:Any) -> CardsRulings:
        return CardsRulings(self.id_type, self.id, **kwargs)


class CardsRulings(ScrypyfallIterableFoundation):
    def __init__(self, id_type:str, id:str = None, code:str = None, number:str = None, **kwargs:Any) -> None:
        allowed_id_types = ['multiverse', 'mtgo', 'arena', 'tcgplayer', 'cardmarket', 'scryfall', 'code']
        if id_type not in allowed_id_types:
            raise ValueError(f"invalid id type: {id}")
        
        if id_type == 'code':
            _url = f'cards/{code}/{number}/rulings'
        elif id_type == 'scryfall':
            _url = f'cards/{id}/rulings'
        else:
            _url = f'cards/{id_type}/{id}/rulings'
        super().__init__(_url)

        if 'headers' in kwargs:
            self.headers.update(kwargs['headers'])

        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        self._get_data_page(validate_params=False, **params)


class CardsOracle(ScrypyfallIterableFoundation):
    def __init__(self, id:str, **kwargs: Any) -> None:
        super().__init__(f'cards/oracle/{id}')
        self.accepted_params.update({
            'format': {'type': str, 'options': ['json', 'text', 'image']},
            'face': {'type': str},
            'version': {'type': str, 'options': IMAGE_VERSION_OPTIONS}
        })

        if 'headers' in kwargs:
            self.headers.update(kwargs['headers'])
        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}

        self._get_data_page(validate_params=False, **params)


    






            


