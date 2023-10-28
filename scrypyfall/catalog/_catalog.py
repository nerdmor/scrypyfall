from typing import NewType

from scrypyfall.foundation import ScrypyfallFoundation
from scrypyfall.foundation import ScrypyfallCollection

class Catalog():
    def __init__(self) -> None:
        self.dummy_foundation = ScrypyfallFoundation('catalog')

    def card_names(self):
        return self.dummy_foundation.make_request('card-names')
    def artist_names(self):
        return self.dummy_foundation.make_request('artist-names')
    def word_bank(self):
        return self.dummy_foundation.make_request('word-bank')
    def creature_types(self):
        return self.dummy_foundation.make_request('creature-types')
    def planeswalker_types(self):
        return self.dummy_foundation.make_request('planeswalker-types')
    def land_types(self):
        return self.dummy_foundation.make_request('land-types')
    def artifact_types(self):
        return self.dummy_foundation.make_request('artifact-types')
    def enchantment_types(self):
        return self.dummy_foundation.make_request('enchantment-types')
    def spell_types(self):
        return self.dummy_foundation.make_request('spell-types')
    def powers(self):
        return self.dummy_foundation.make_request('powers')
    def toughnesses(self):
        return self.dummy_foundation.make_request('toughnesses')
    def loyalties(self):
        return self.dummy_foundation.make_request('loyalties')
    def watermarks(self):
        return self.dummy_foundation.make_request('watermarks')
    def keyword_abilities(self):
        return self.dummy_foundation.make_request('keyword-abilities')
    def keyword_actions(self):
        return self.dummy_foundation.make_request('keyword-actions')
    def ability_words(self):
        return self.dummy_foundation.make_request('ability-words')
    def supertypes(self):
        return self.dummy_foundation.make_request('supertypes')
