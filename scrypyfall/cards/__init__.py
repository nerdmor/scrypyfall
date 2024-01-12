"""Wrapper for the card endpoints in Scryfall."""

from ._cards import Cards

cards = Cards()

__all__ = ['cards']