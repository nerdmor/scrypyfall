from typing import Any, NewType

# Custom libraries
from scrypyfall.foundation import ScrypyfallFoundation

ScrypyfallCatalog = NewType('ScrypyfallCatalog', list)


class Catalog():
    """Generic wrapper for the /catalog/* endpoints
    """
    def __init__(self) -> None:
        self.dummy_foundation = ScrypyfallFoundation('catalog')
    
    def __call__(self, endpoint:str, **kwargs: Any) -> ScrypyfallCatalog:
        """Calls a given catalog endpoint
        
        This is a wrapper for all the internal, endpoint-specific, named
        methods

        Args:
            endpoint (str): endpoint to be called

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        endpoint = endpoint.lower().strip().replace('-', '_')
        func = getattr(self, endpoint)
        return func(**kwargs)
        

    def card_names(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/card-names endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('card-names', **kwargs)
    def artist_names(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/artist-names endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('artist-names', **kwargs)
    def word_bank(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/word-bank endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('word-bank', **kwargs)
    def creature_types(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/creature-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('creature-types', **kwargs)
    def planeswalker_types(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/planeswalker-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('planeswalker-types', **kwargs)
    def land_types(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/land-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('land-types', **kwargs)
    def artifact_types(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/artifact-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('artifact-types', **kwargs)
    def enchantment_types(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/enchantment-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('enchantment-types', **kwargs)
    def spell_types(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/spell-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('spell-types', **kwargs)
    def powers(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/powers endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('powers', **kwargs)
    def toughnesses(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/toughnesses endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('toughnesses', **kwargs)
    def loyalties(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/loyalties endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('loyalties', **kwargs)
    def watermarks(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/watermarks endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('watermarks', **kwargs)
    def keyword_abilities(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/keyword-abilities endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('keyword-abilities', **kwargs)
    def keyword_actions(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/keyword-actions endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('keyword-actions', **kwargs)
    def ability_words(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/ability-words endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('ability-words', **kwargs)
    def supertypes(self, **kwargs) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/supertypes endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('supertypes', **kwargs)
