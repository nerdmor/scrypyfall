"""Wraps and makes settings accessible

Returns:
    _type_: _description_
"""
    
class Settings():
    """Wrapper for settings to be used in a dict-like fashion
    
    Attributes:
        sleep_time (float): time, in seconds, to wait before each request to
            prevent clogging the servers. Defaults to 0.1
        protocol (str): the protocol to be used when calling Scryfall. Please
            don't use anything other than https. Defaults to https.
        domain (str): the domain to use to call Scryfall. Defaults to 
            api.scryfall.com
        chunk_size (int): number of bytes to read at a time when downloading
            bulk objects. Defaults to 8192.
        headers (dict): default headers to use in all requests. Should be useful
            when logged in.
        lazy_loading (bool): if set to False, will load all pages when making a
            search or getting some other kind of paginated content. Defaults to
            True
        
    """    
    def __init__(self) -> None:
        self.sleep_time = 0.1
        self.protocol = 'https'  # protocol to be used. Should never use anything
        self.domain = 'api.scryfall.com'
        self.chunk_size = 8192
        self.headers = {}
        self.lazy_loading = True

    def __getitem__(self, key:str) -> any:
        """Allows this classe's attributes to be read like a dict

        Args:
            key (str): key to be accessed

        Returns:
            any: value of the attribute
        """        
        return getattr(self, key)

settings = Settings()