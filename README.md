# scrypyfall
A Python Scryfall API wrapper. Inspired by XXX's Scrython library.

This library tries to emulate as closely as possible [Scryfall's API](https://scryfall.com/docs/api) syntax, allowing for easy integration.


# Dependencies
- `requests` >= 2.31.0

## Usage
Import the library using `import scrypyffall`. It is not recommended to import *.

The submodules/packages try to emulate the endpoints syntax. See "Endpoint Reference" below for a full list.

Return objects are always a `dict` or `list`-compatible object. See "Response Objects" below for more 

```
>>>> import scrypyfall
>>>> snails = scrypyfall.cards.search(q='t:snail c:b cmc<3', order='name')
>>>> for card in snails:
>>>>    print(f"{card['name']}  {card['mana_cost']}")
Skullcap Snail  {1}{B}
```

## Response Objects
Returns/responses from the library are meant to simplify usage as much as possible. `dicts` or `lists` will be returned most of the cases; when not, it will be one of the following objects:

### ScrypyfallFoundation
This Class is used when we are retrieving records that, according to Scryfall, cannot be paginated.
This behaves like a `dict`. When retrieving a key, it will try first to get the data from `self.data` (which holds the data pulled from the API); failing that, it will return its own attributes.

### ScrypyfallIterableFoundation
This Class is used when we are retrieving records that, according to Scryfall, can be paginated.
It behaves both like a `list` and a `dict`.
* If called as an interator, will yield elements of `self.data`.
* If accessed as a dict with an `int` key, will return elements of self.data.
* If accessed as a dict with and `str` key, will return attributes of self.

This object has lazy loading; both when iterating and when getting index keys, the object will load the next page until that index is present. This can be circumvented with either calling the objects's `.load()` function or with setting `settings['lasy_loading']` to `False` (see below).
```
>>>> import scrypyfall
>>>> sets = scrypyfall.sets()
>>>> print(s['total'])
865
>>>> for s in sets:
>>>>     print(s['name'])
Fallout
Fallout Tokens    
Ravnica Remastered
```

## Settings
Once the library is imported, you can change its behavior by changing values in `scrypyfall.settings`.  
Changing settings values will affect new requests, but not already-instantiated objects.

```
>>>> import scrypyfall
>>>> scrypyfall.settings.sleep_time = 1.0
```

Below is a reference of all settings:
| **Setting** | **Data type** | **Default** | **Description** |
| ----------- | ------------- | ----------- | --------------- |
| `sleep_time` | `float` | 0.1 | Time, in seconds that the API will wait before making a call. Scryfall [requests](https://scryfall.com/docs/api#rate-limits-and-good-citizenship) that you always wait at least 100ms |
| `protocol` | `str` | https | Protocol to use when calling the API. No calls to http should succeed, but I won't stop you trying |
| `domain` | `str` | api.scryfall.com | Domain to call. If someone ever makes a Scryfall-compatible API |
| `chunk_size` | `int` | 8192 | number of bytes per chunk to be used when downloading bulk files |
| `headers` | `dict` | `{}` | Headers that will be sent in every call. May be useful for logged-in features someday. |
| `lazy_loading` | `bool` | `True` | If set to `False`, will force all iterable objects to load completely upon calling. This can impact performance. |


## Endpoint Reference
The table below shows all current Scryfall endpoints and how they relate Scrypyfall methods.  
The domain `https://api.scryfall.com` is ommited for brevity and legibility, as is the package name `scrypyfall`.

| **Group** | **Endpoint** | **Method** | **Parameters** | ** Notes ** |
| -------------- | ------------ | ---------- | -------------- | ----------- |
| **Sets** |  |  |  |  | 
|  | [/sets](https://scryfall.com/docs/api/sets/all) | `.sets()` | `None` | |
|  | [/sets/:code](https://scryfall.com/docs/api/sets/code) | `.sets.code({set_code})` | set_code (`str`) | Alias: `.sets(code={set_code})` |
|  | [/sets/tcgplayer/:id](https://scryfall.com/docs/api/sets/tcgplayer) | `.sets.tcgplayer.id({tcgplayer_set_id})` | tcgplayer_set_id (`int`) | Alias: `.sets.tcgplayer(id={tcgplayer_set_id})` |
|  | [/sets/:id](https://scryfall.com/docs/api/sets/id) | `.sets.id({set_scryfall_id})` | set_scryfall_id (`str`) | Alias: `.sets(id={set_scryfall_id})` |
| **Cards** |  |  |  |  | 
|  | [/cards/search](https://scryfall.com/docs/api/cards/search) | `.cards.search(q)` | q (`str`) | Check  method and/or endpoint documentation for full list of parameters |
|  | [/cards/named](https://scryfall.com/docs/api/cards/named) | `.cards.named(exact={query}, fuzzy={query})` | query (`str`) | `exact` and `fuzzy` cannot be combined. <br /> Check  method and/or endpoint documentation for full list of parameters |
|  | [/cards/autocomplete](https://scryfall.com/docs/api/cards/autocomplete) | `.cards.autocomplete({q})` | q (`str`) |   |
|  | [/cards/random](https://scryfall.com/docs/api/cards/random) | `.cards.random({q})` | q(`str`) | Check method and/or endpoint documentation for full list of parameters |
|  | [/cards/collection](https://scryfall.com/docs/api/cards/collection) | `.cards.collection()` | `None` |  |
|  | [/cards/:code/:number](https://scryfall.com/docs/api/cards/collector) | `.cards.code({set_code}).number({card_number})` | set_code (`str`);<br /> card_number (`str`) | Alias: `.cards.code({set_code}, {card_number})` |
|  | [/cards/:code/:number/:lang](https://scryfall.com/docs/api/cards/collector) | `.cards.code({set_code}).number({card_number}).lang({lang_code})` | set_code (`str`);<br /> card_number (`str`);<br /> lang_code (`str`) | Alias: `.cards.code({set_code}, {card_number}, {lang_code})` |
|  | [/cards/multiverse/:id](https://scryfall.com/docs/api/cards/multiverse) | `.cards.multiverse(id={id})` | id (`int`) | Alias: `.cards.multiverse.id({id})` |
|  | [/cards/mtgo/:id](https://scryfall.com/docs/api/cards/mtgo) | `.cards.mtgo(id={id})` | id (`int`) | Alias: `.cards.mtgo.id({id})` |
|  | [/cards/arena/:id](https://scryfall.com/docs/api/cards/arena) | `.cards.arena(id={id})` | id (`int`) | Alias: `.cards.arena.id({id})` |
|  | [/cards/tcgplayer/:id](https://scryfall.com/docs/api/cards/tcgplayer) | `.cards.tcgplayer(id={id})` | id (`int`) | Alias: `.cards.tcgplayer.id({id})` |
|  | [/cards/cardmarket/:id](https://scryfall.com/docs/api/cards/cardmarket) | `.cards.cardmarket(id={id})` | id (`int`) | Alias: `.cards.cardmarket.id({id})` |
|  | /oracle/:id | `.cards.oracle({id})` | id (`str`) | Undocumented endpoint. |
|  | [/cards/:id](https://scryfall.com/docs/api/cards/id) | `.cards.id({id})` | id (`str`) | Alias: `.cards({id})` |
| **Rulings** |  |  |  |  | 
|  | [/cards/multiverse/:id/rulings](https://scryfall.com/docs/api/rulings/multiverse) | `.cards.multiverse({id}).rulings()` | id (`int`) |  |
|  | [/cards/mtgo/:id/rulings](https://scryfall.com/docs/api/rulings/mtgo) | `.cards.mtgo({id}).rulings()` | id (`int`) |  |
|  | [/cards/arena/:id/rulings](https://scryfall.com/docs/api/rulings/arena) | `.cards.arena({id}).rulings()` | id (`int`) |  |
|  | [/cards/:code/:number/rulings](https://scryfall.com/docs/api/rulings/collector) | `.cards.code({set_code}).number({card_number}).rulings()` | set_code (`str`);<br /> card_number (`str`) | Alias: `.cards.code({set_code}, {card_number}).rulings()` |
|  | [/cards/:id/rulings](https://scryfall.com/docs/api/rulings/id) | `.cards({id}).rulings()` | id (`str`) | Alias: `.cards.id({id}).rulings()` |
| **Symbols** |  |  |  |  | 
|  | [/symbology](https://scryfall.com/docs/api/card-symbols/all) | `.symbology()` |  |  |
|  | [/symbology/parse-mana](https://scryfall.com/docs/api/card-symbols/parse-mana) | `.symbology.parse_mana({cost})` | cost (`str`) |  |
| **Catalogs** |  |  |  |  | 
|  | [/catalog/card-names](https://scryfall.com/docs/api/catalogs/card-names) | `.catalog.card_names()` |  |  |
|  | [/catalog/artist-names](https://scryfall.com/docs/api/catalogs/artist-names) | `.catalog.artist_names()` |  |  |
|  | [/catalog/word-bank](https://scryfall.com/docs/api/catalogs/word-bank) | `.catalog.word_bank()` |  |  |
|  | [/catalog/creature-types](https://scryfall.com/docs/api/catalogs/creature-types) | `.catalog.creature_types()` |  |  |
|  | [/catalog/planeswalker-types](https://scryfall.com/docs/api/catalogs/planeswalker-types) | `.catalog.planeswalker_types()` |  |  |
|  | [/catalog/land-types](https://scryfall.com/docs/api/catalogs/land-types) | `.catalog.land_types()` |  |  |
|  | [/catalog/artifact-types](https://scryfall.com/docs/api/catalogs/artifact-types) | `.catalog.artifact_types()` |  |  |
|  | [/catalog/enchantment-types](https://scryfall.com/docs/api/catalogs/enchantment-types) | `.catalog.enchantment_types()` |  |  |
|  | [/catalog/spell-types](https://scryfall.com/docs/api/catalogs/spell-types) | `.catalog.spell_types()` |  |  |
|  | [/catalog/powers](https://scryfall.com/docs/api/catalogs/powers) | `.catalog.powers()` |  |  |
|  | [/catalog/toughnesses](https://scryfall.com/docs/api/catalogs/toughnesses) | `.catalog.toughnesses()` |  |  |
|  | [/catalog/loyalties](https://scryfall.com/docs/api/catalogs/loyalties) | `.catalog.loyalties()` |  |  |
|  | [/catalog/watermarks](https://scryfall.com/docs/api/catalogs/watermarks) | `.catalog.watermarks()` |  |  |
|  | [/catalog/keyword-abilities](https://scryfall.com/docs/api/catalogs/keyword-abilities) | `.catalog.keyword_abilities()` |  |  |
|  | [/catalog/keyword-actions](https://scryfall.com/docs/api/catalogs/keyword-actions) | `.catalog.keyword_actions()` |  |  |
|  | [/catalog/ability-words](https://scryfall.com/docs/api/catalogs/ability-words) | `.catalog.ability_words()` |  |  |
|  | [/catalog/supertypes](https://scryfall.com/docs/api/catalogs/supertypes) | `.catalog_supertypes()` |  |  |
| **Bulk Data** |  |  |  |  | 
|  | [/bulk-data](https://scryfall.com/docs/api/bulk-data/all) | `.bulk_data()` |  |  |
|  | [/bulk-data/:id](https://scryfall.com/docs/api/bulk-data/id) | `.bulk_data(id={id})` | id (`str`) |  |
|  | [/bulk-data/:type](https://scryfall.com/docs/api/bulk-data/type) | `.bulk_data(type_={type})` | type (`str`) |  |
