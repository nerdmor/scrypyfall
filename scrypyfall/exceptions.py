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

class ScrypyFallTooFewIdentifiersException(ScrypyfallException):
    pass
class ScrypyFallTooManyIdentifiersException(ScrypyfallException):
    pass
class ScrypyFallInvalidIdentifiersException(ScrypyfallException):
    pass