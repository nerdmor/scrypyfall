from typing import NewType

# Custom libraries
from scrypyfall.foundation import ScrypyfallFoundation
from scrypyfall.foundation import ScrypyfallCollection # TODO: remove this

ScrypyfallCatalog = NewType('ScrypyfallCatalog', list)


class Catalog():
    def __init__(self) -> None:
        # TODO: add header updating
        self.dummy_foundation = ScrypyfallFoundation('catalog')

    def card_names(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/card-names endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('card-names')
    def artist_names(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/artist-names endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('artist-names')
    def word_bank(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/word-bank endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('word-bank')
    def creature_types(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/creature-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('creature-types')
    def planeswalker_types(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/planeswalker-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('planeswalker-types')
    def land_types(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/land-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('land-types')
    def artifact_types(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/artifact-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('artifact-types')
    def enchantment_types(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/enchantment-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('enchantment-types')
    def spell_types(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/spell-types endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('spell-types')
    def powers(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/powers endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('powers')
    def toughnesses(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/toughnesses endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('toughnesses')
    def loyalties(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/loyalties endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('loyalties')
    def watermarks(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/watermarks endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('watermarks')
    def keyword_abilities(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/keyword-abilities endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('keyword-abilities')
    def keyword_actions(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/keyword-actions endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('keyword-actions')
    def ability_words(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/ability-words endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('ability-words')
    def supertypes(self) -> ScrypyfallCatalog:
        """Wrapper for the /catalog/supertypes endpoint

        Returns:
            ScrypyfallCatalog: a IterableResponse-derived object
        """
        return self.dummy_foundation.make_request('supertypes')
