class Settings():
    def __init__(self) -> None:
        self.sleep_time = 0.1  # time, in seconds, to wait before each request to prevent clogging the servers
        self.protocol = 'https'
        self.domain = 'api.scryfall.com'
        self.chunk_size = 8192
        self.headers = {}
    
    def __getitem__(self, key):
        return getattr(self, key)

settings = Settings()