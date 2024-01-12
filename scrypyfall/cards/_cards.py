"""Wrapper for the card functions in Scryfall.

This depends heavily in foundation.py and uses several "child" objects to
emulate Scryfall's API structure.
"""

# standard libraries
from typing import Any
from typing import NewType

# custom libraries
from scrypyfall.foundation import ScrypyfallFoundation
from scrypyfall.foundation import ScrypyfallIterableFoundation
from scrypyfall.foundation import ScrypyfallList
from scrypyfall.foundation import IMAGE_VERSION_OPTIONS
from scrypyfall.exceptions import ScrypyFallTooFewIdentifiersException
from scrypyfall.exceptions import ScrypyFallTooManyIdentifiersException
from scrypyfall.exceptions import ScrypyFallInvalidIdentifiersException

# settings
from ..settings import settings


CardsSearch = NewType('CardsSearch', list)
CardsNamed = NewType('CardsNamed', list)
CardsAutocomplete = NewType('CardsAutocomplete', dict)
CardsRandom = NewType('CardsRandom', dict)
CardsCollection = NewType('CardsCollection', dict)
CardsCodeNumber = NewType('CardsCodeNumber', dict)
CardsById = NewType('CardsMultiverse', dict)
CardsOracle = NewType('CardsOracle', dict)
CardsRulings = NewType('CardsRulings', list)

class Cards():
    """Wrapper class for card functions. Acts as a proxy to the smaller objects.
    
    Attributes:
        multiverse (CardsById): represents the objects that can be gotten
            through a Multiverse ID
        mtgo (CardsById): represents the objects that can be gotten through a
            MtGO ID
        arena (CardsById): represents the objects that can be gotten through an
            Arena ID
        tcgplayer (CardsById): represents the objects that can be gotten through
            a TCGPlayer ID
        cardmarket (CardsById): represents the objects that can be gotten
            through a Cardmarket ID
        _scryfall (CardsById): represents the objects that can be gotten
            through a Scryfall ID
    """
    def __init__(self) -> None:
        self.multiverse = CardsById('multiverse')
        self.mtgo = CardsById('mtgo')
        self.arena = CardsById('arena')
        self.tcgplayer = CardsById('tcgplayer')
        self.cardmarket = CardsById('cardmarket')
        self._scryfall = CardsById('scryfall')

    def __call__(self, id:str, **kwargs: Any) -> CardsById:
        """Gets a card by its Scryfall ID.
    
        Allows the class to be called as a function, to emulate the "/cards/:id"
        endpoint syntax.
        This is an alias of self.id(), and any kwargs will be passed to it.

        Args:
            id (str): card ID to be gotten.

        Returns:
            CardsById: A ScrypyfallFoundation-derived object
        """
        return self.id(id, **kwargs)
    
    def id(self, id:str, **kwargs: Any) -> CardsById:
        """Gets a card by its Scryfall ID. Wraps /cards/:id
    
        This is an alias of self._scryfall(), which is an instance of CardsById
        and any kwargs will be passed to it.

        Args:
            id (str): card ID to be gotten.

        Returns:
            CardsById: A ScrypyfallFoundation-derived object
        """
        return self._scryfall(id, **kwargs)

    def search(self, q:str, **kwargs: Any) -> CardsSearch:
        """Searches for cards, using a Scryfall-compatible search criteria. Wraps /cards/search.
        
        This instances CardSearch. Please see kwagrs there.

        Args:
            q (str): An Scryfall-compatible search string.

        Returns:
            CardsSearch: A ScrypyfallIterableFoundation-derived object
        """
        return CardsSearch(q, **kwargs)
    
    def named(self, **kwargs: Any) -> CardsNamed:
        """Searches for cards with the given name. Wraps /cards/named.
        
        This instances CardsNamed. Please see kwargs there.

        Returns:
            CardsNamed: A ScrypyfallIterableFoundation-derived object.
        """
        return CardsNamed(**kwargs)[0]
    
    def autocomplete(self, q:str, **kwargs: Any) -> CardsAutocomplete:
        """Gives a list of possible autocompletes for a given string. Wraps /cards/autocomplete.
        
        This instances CardsAutocomplete. Please see kwargs there.

        Args:
            q (str): Partial name of a card to get autocompletions for.

        Returns:
            CardsAutocomplete: A ScrypyfallFoundation-derived object.
        """
        return CardsAutocomplete(q, **kwargs).data
    
    def random(self, **kwargs: Any) -> CardsRandom:
        """Gets a random card. Wraps /cards/random.
        
        This instances CardsRandom. Please see kwargs there.

        Returns:
            CardsRandom: A ScrypyfallFoundation-derived object.
        """
        return CardsRandom(**kwargs).data
    
    def collection(self, identifiers:list, **kwargs: Any) -> CardsCollection:
        """Gets a collection of cards. Wraps /cards/collection.
        
        This instances CardsCollection. Please see kwargs there.

        Args:
            identifiers (list): Scryfall identifiers. Please see
                https://scryfall.com/docs/api/cards/collection#card-identifiers 
                for details

        Returns:
            CardsCollection: A ScrypyfallIterableFoundation-derived object.
        """
        return CardsCollection(identifiers, **kwargs)
    
    def code(self, code:str, number:str =None, lang:str =None, **kwargs:Any) -> CardsCodeNumber:
        """Gets a specific version of a card, given its set code and number. Wraps /cards/:code/:number(/:lang).
        
        Though number is optional, it is needed to actually get the data, but by
        allowing a None value, it allows the clas to be used as
        .code('xln').number(96), which is more natual for some.
        This instances CardsCodeNumber. Please see kwargs there.

        Args:
            code (str): The three to five-letter set code of the desired card.
            number (str, optional): The collector number. If None, the returned
                object will need to have.number() called. Defaults to None.
            lang (str, optional): If provided, will return data for the cards in
                that language. Defaults to None.

        Returns:
            CardsCodeNumber: A ScrypyfallFoundation-derived object.
        """
        return CardsCodeNumber(code, number=number, lang=lang, **kwargs)
    
    def oracle(self, id:str, **kwargs:Any) -> CardsOracle:
        """Gets a card through its Oracle ID. This is a hidden endpoint.
        
        This instances CardsOracle. Please see kwargs there.

        Args:
            id (str): Oracle Id of dthe desired card.

        Returns:
            CardsOracle: A ScrypyfallIterableFoundation-derived object.
        """
        return CardsOracle(id, **kwargs).data
    


class CardsSearch(ScrypyfallIterableFoundation):
    """Wraps the /Cards/Search endpoint, handling requests and responses.
    """
    def __init__(self, q:str|dict, **kwargs: Any) -> None:
        """Initializes the object.

        Args:
            q (str | dict): A Scryfall search. It will accept both a direct
                string or a dict, with key-value pairs.
            unique (str, optional): If provided, will return cards as a unique
                set around the given field.
                Accepted values: ['cards', 'art', 'print']
            order (str, optional): If provided, will order the results by this
                field. Accepted values: ['name', 'set', 'released', 'rarity',
                'color', 'usd', 'tix', 'eur', 'cmc', 'power', 'toughness',
                'edhrec', 'penny', 'artist', 'review']
            dir (str, optional): If provided along with order, will set the
                direction in which the results are ordered.
                Accepted values: ['auto', 'asc', 'desc']
            include_extras (bool, optional): If True, extra cards (tokens,
                planes, etc) will be included. Equivalent to adding
                include:extras to the fulltext search.
            include_multilingual (bool, optional): If True, cards in every
                language supported by Scryfall will be included.
            include_variations (bool, optional): If True, rare care variants
                will be included, like the Hairy Runesword.
            format (str, optional): The data format to return.
                Accepted values: ['json', 'csv'].
            headers (dict, optional): Any headers that should be passed along
                with the requests made.
        """
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
        if settings.lazy_loading is False:
            self.load(validate_params=False, **params)
        else:
            self._get_data_page(validate_params=False, **params)


class CardsNamed(ScrypyfallIterableFoundation):
    """Wraps the /Cards/Named endpoint, handling requests and responses.
    """
    def __init__(self, **kwargs) -> None:
        """Initializes the object.
        
        Args:
            exact (str, optional): The exact card name to search for, case
                insenstive. Either this or 'fuzzy' must be provided, but not
                both.
            fuzzy (str, optional): A fuzzy card name to search for. Either this
                or 'exact' must be provided, but not both.
            set (str, optional): A set code to limit the search to one set. 
            format (str, optional): The data format to return.
                Accepted values: ['json', 'csv', 'image'].
            face (str, optional): If using the image format and this parameter
                has the value 'back', the back face of the card will be returned.
                Will return a 422 if this card has no back face. 
            version (str, optional): The image version to return when using the
                image format. See values in IMAGE_VERSION_OPTIONS.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.

        Raises:
            ValueError: when the 'exact' and 'fuzzy' are missing or are both
                provided at once.
        """
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
        if settings.lazy_loading is False:
            self.load(validate_params=False, **params)
        else:
            self._get_data_page(validate_params=False, **params)
        

class CardsAutocomplete(ScrypyfallFoundation):
    """Wraps the /Cards/Autocomplete endpoint, handling requests and responses.
    """
    def __init__(self, q:str, **kwargs: Any) -> None:
        """Initializes the object.

        Args:
            q (str): The string to autocomplete.
            include_extras (bool, optional): If True, extra cards (tokens,
                planes, etc) will be included. Equivalent to adding
                include:extras to the fulltext search.
            headers (dict, optional): Any headers that should be passed along
                            with the requests made.
        """
        super().__init__('cards/autocomplete')
        self.accepted_params.update({
            'q': {'type': str},
            'include_extras': {'type': bool}
        })

        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        params['q'] = q
        self.data = self.make_request(params=params, validate_params=False, headers=kwargs.get('headers'))


class CardsRandom(ScrypyfallFoundation):
    """Wraps the /Cards/Random endpoint, handling requests and responses.
    """
    def __init__(self, **kwargs: Any) -> None:
        """Initializes the object.
        
        Args:
            q (str, optional): A fulltext search query to filter the pool of
                random cards.
            format (str, optional): The data format to return.
                Accepted values: ['json', 'csv'].
            face (str, optional): If using the image format and this parameter
                has the value 'back', the back face of the card will be returned.
                Will return a 422 if this card has no back face.
            version (str, optional): The image version to return when using the
                image format. See values in IMAGE_VERSION_OPTIONS.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.
        """
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
    """Wraps the /Cards/Collection endpoint, handling requests and responses.
    """
    def __init__(self, identifiers:list, **kwargs: Any) -> None:
        """_summary_

        Args:
            identifiers (list): List of dicts with identifiers. Each card
                identifier must be a dict with one or more of the keys:
                ["id", 'mtgo_id', 'multiverse_id', 'oracle_id',
                'illustration_id', 'name', 'set', 'collector_number']
            headers (dict, optional): Any headers that should be passed along
                with the requests made.
            

        Raises:
            ScrypyFallTooFewIdentifiersException: When not enough identifiers are
                provided.
            ScrypyFallTooManyIdentifiersException: When more than 75 identifiers are
                provided.
            ScrypyFallInvalidIdentifiersException: When the given identifiers are invalid
        """
        super().__init__('cards/collection')

        if not identifiers:
            raise ScrypyFallTooFewIdentifiersException("A non-empty list of identifiers is needed")

        if len(identifiers) > 75:
            raise ScrypyFallTooManyIdentifiersException(f"A maximum of 75 identifiers are allowed. {len(identifiers)} provided.")

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
                raise ScrypyFallInvalidIdentifiersException('All elements in an identifier array must be dicts')
            for k, v in ide.items():
                if v is None:
                    raise ScrypyFallInvalidIdentifiersException(f"Null identifiers are not allowed")
                if k not in allowed_keys:
                    raise ScrypyFallInvalidIdentifiersException(f"Invalid identifier '{k}' in list")
                if not isinstance(v, allowed_keys[k]):
                    raise ScrypyFallInvalidIdentifiersException(f"Values of identifiers '{k}' must be {allowed_keys[k]}, {type(v)} provided")
                if k == 'set' and 'name' not in ide and 'collector_number' not in ide:
                    raise ScrypyFallInvalidIdentifiersException("'set' identifiers must always have a collector number or name in the same request")
        
        if 'headers' in kwargs:
            self.headers.update(kwargs['headers'])
        
        self.has_more = False
        self.not_found = []

        if settings.lazy_loading is False:
            self.load(payload={'identifiers': identifiers}, **kwargs)
        else:
            self._get_data_page(payload={'identifiers': identifiers}, **kwargs)
    
    def asdict(self) -> dict:
        """Returns a dict representation of self.

        Returns:
            dict: a dict representation of self.
        """
        return {
            'has_more': self.has_more,
            'data': self.data,
            'total': self.total,
            'not_found': self.not_found
        }
        
    def _get_data_page(self, **kwargs:Any) -> None:
        """Internal. Fills self.data with data returned by the API.
        
        Args:
            payload (dict): data to be sent to the endpoint.

        Raises:
            ValueError: when the request is missing a payload.
            RuntimeError: when the response from Scryfall is invalid.
        """
        if self.data or self.not_found:
            return
        if 'payload' not in kwargs:
            raise ValueError('payload is mandatory')

        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        new_data = super().make_request(
            params=params,
            validate_params=False,
            method='post',
            json_payload=kwargs['payload']
        )
        if isinstance(new_data, ScrypyfallList):
            self.data += new_data.data
            self.total = len(self.data)
            self.not_found = new_data.not_found
        else:
            raise RuntimeError('invalid response from Scryfall. Could not process response as a list')
    
        
class CardsCodeNumber(ScrypyfallFoundation):
    """Wraps the /cards/:code/:number(/:lang) endpoint, handling requests and responses.
    
    Also provides methods to access /cards/:code/:number/rulings.
    """
    def __init__(self, code:str, **kwargs:Any) -> None:
        """initializes the object.

        Args:
            code (str): Three to five-letter set code of the desired card.
            number (str, optional): The collector number of the desired card. If
                None, the returned object will need to have.number() called.
            lang (str, optional): If provided, will return data for the cards in
                that language.
            format (str, optional): The data format to return.
                Accepted values: ['json', 'csv', 'image'].
            version (str, optional): The image version to return when using the
                image format. See values in IMAGE_VERSION_OPTIONS.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.
        """
        super().__init__(f'cards/{code}')
        
        # TODO: add headers updating

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
        """Internal. Wraps ScrypyfallFoundation.make_request() to allow for precise URL building. 
        
        kwargs are inherited from self.__init__()
        """
        if self.lan is None:
            self.url = self._build_base_url(f'cards/{self.code}/{self.num}')
        else:
            self.url = self._build_base_url(f'cards/{self.code}/{self.num}/{self.lan}')
        
        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        if not params:
            params = None
        self.data = self.make_request(validate_params=False, params=params)

    
    def number(self, number:int|str, **kwargs:Any) -> CardsCodeNumber:
        """Sets self.num and calls _request_wrapper. Allows for users to do CardsCodeNumber('set').number(69)

        Args:
            number (int | str): The collector number of the desired card.

        Returns:
            CardsCodeNumber: self
        """
        self.num = str(number)
        self._request_wrapper(**kwargs)
        return self

    def lang(self, lang:str, **kwargs:Any) -> CardsCodeNumber:
        """sets self.lan and tries to get data from the API.

        Args:
            lang (str): Language in which you want the card data.

        Raises:
            RuntimeError: When trying to call .lang without setting a collector
                number first, either during instantiation or by calling .number()

        Returns:
            CardsCodeNumber: self
        """
        self.lan = lang
        if self.num is None:
            raise RuntimeError('trying to request a card of a language without setting a number')
        self._request_wrapper(**kwargs)
        return self
    
    def rulings(self, **kwargs: Any) -> CardsRulings:
        """Wrapper for /cards/:code/:number/rulings.
        
        This instantiates CardsRulings. Please see kwargs there.
        
        Raises:
            RuntimeError: When trying to call .rulings without setting a
            collector number first, either during instantiation or by calling
            .number()

        Returns:
            CardsRulings: A ScrypyfallIterableFoundation-derived object
        """
        if self.num is None:
            raise RuntimeError('trying to request rulings for a card without setting a number')
        return CardsRulings('code', code=self.code, number=self.num, **kwargs)


class CardsById(ScrypyfallFoundation):
    """Wrapper for several endpoints where a card is retrieved by its ID.
    """
    def __init__(self, id_type:str, **kwargs:Any) -> None:
        """Initializes the object

        Args:
            id_type (str): kind of card ID that will be used. Accepted values:
                ['multiverse', 'mtgo', 'arena', 'tcgplayer', 'cardmarket',
                'scryfall', 'code']
            format (str, optional): The data format to return.
                Accepted values: ['json', 'csv', 'image'].
            face (str, optional): If using the image format and this parameter
                has the value 'back', the back face of the card will be returned.
                Will return a 422 if this card has no back face. 
            version (str, optional): The image version to return when using the
                image format. See values in IMAGE_VERSION_OPTIONS.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.

        Raises:
            ValueError: when the id_type has an invalid value.
        """
        allowed_id_types = ['multiverse', 'mtgo', 'arena', 'tcgplayer', 'cardmarket', 'scryfall']
        if id_type not in allowed_id_types:
            raise ValueError(f"invalid id type: {id}")
        
        if id_type == 'scryfall':
            _url = 'cards'
        else:
            _url = f'cards/{id_type}'
        super().__init__(_url)
        
        # TODO: add headers updating

        self.accepted_params.update({
            'format': {'type': str, 'options': ['json', 'text', 'image']},
            'face': {'type': str},
            'version': {'type': str, 'options': IMAGE_VERSION_OPTIONS}
        })

        self.id = None
        self.id_type = id_type
    
    def __call__(self, id:int|str, **kwargs) -> CardsById:
        """Allows the object to be called, filling self.data
        
        kwargs are the same as when initializing the object.

        Args:
            id (int | str): ID of the card.

        Returns:
            CardsById: self
        """
        self.id = str(id)
        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        if not params:
            params = None
        self.data = self.make_request(self.id, params=params, headers=kwargs.get('headers'), validate_params=False)
        return self
    
    def rulings(self, **kwargs:Any) -> CardsRulings:
        """Gets rulings for the cards.
        
        This is instances CardsRulings. Please see kwargs there.
        
        Raises:
            ValueError: when this hasn't been called and thus self.id is None.

        Returns:
            CardsRulings: A ScrypyfallIterableFoundation-derived object.
        """
        if self.id is None:
            raise ValueError('Trying to call rulings() in a card without an id')
        return CardsRulings(self.id_type, self.id, **kwargs)


class CardsRulings(ScrypyfallIterableFoundation):
    """Wrapper for /cards/:code/:number/rulings.
    """
    def __init__(self, id_type:str, id:str = None, code:str = None, number:str = None, **kwargs:Any) -> None:
        """Initializes the object

        Args:
            id_type (str): kind of card ID that will be used. Accepted values:
                ['multiverse', 'mtgo', 'arena', 'tcgplayer', 'cardmarket',
                'scryfall', 'code']
            id (str, optional): ID of the card for which we want the rulings.
                It is mandatory when using any id_type except for 'code'.
            code (str, optional): Three to five-letter set code of the desired
                card. Mandatory when using id_type == 'code'
            number (str, optional): The collector number of the desired card.
                Mandatory when using id_type == 'code'
            headers (dict, optional): Any headers that should be passed along
                with the requests made.

        Raises:
            ValueError: When the id_type is of an unknown value
            ValueError: When id_type == 'code' and code and number are not provided.
            ValueError: When id is missing while using other identifiers
        """
        allowed_id_types = ['multiverse', 'mtgo', 'arena', 'tcgplayer', 'cardmarket', 'scryfall', 'code']
        if id_type not in allowed_id_types:
            raise ValueError(f"invalid id type: {id}")
        
        if id_type == 'code':
            if code is None or number is None:
                raise ValueError(f"'code' and/or 'number' are missing when id_type is 'code'")
            _url = f'cards/{code}/{number}/rulings'
        elif id is None:
            raise ValueError(f"'id' is missing when id_type requires it")
        elif id_type == 'scryfall':
            _url = f'cards/{id}/rulings'
        else:
            _url = f'cards/{id_type}/{id}/rulings'
        super().__init__(_url)

        if 'headers' in kwargs:
            self.headers.update(kwargs['headers'])

        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}
        if settings.lazy_loading is False:
            self.load(validate_params=False, **params)
        else:
            self._get_data_page(validate_params=False, **params)


class CardsOracle(ScrypyfallIterableFoundation):
    """Wrapper for the /oracle/id hidden endpoint
    """
    def __init__(self, id:str, **kwargs: Any) -> None:
        """Initializes the object

        Args:
            id (str): oracle ID of the desired card
            format (str, optional): The data format to return.
                Accepted values: ['json', 'csv', 'image'].
            face (str, optional): If using the image format and this parameter
                has the value 'back', the back face of the card will be returned.
                Will return a 422 if this card has no back face. 
            version (str, optional): The image version to return when using the
                image format. See values in IMAGE_VERSION_OPTIONS.
            headers (dict, optional): Any headers that should be passed along
                with the requests made.
        """
        super().__init__(f'cards/oracle/{id}')
        self.accepted_params.update({
            'format': {'type': str, 'options': ['json', 'text', 'image']},
            'face': {'type': str},
            'version': {'type': str, 'options': IMAGE_VERSION_OPTIONS}
        })

        if 'headers' in kwargs:
            self.headers.update(kwargs['headers'])
        params = {k:v for k, v in kwargs.items() if self._validate_param(k, v)}

        if settings.lazy_loading is False:
            self.load(validate_params=False, **params)
        else:
            self._get_data_page(validate_params=False, **params)
