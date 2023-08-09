from enum import Enum


class CollectionStatus(str, Enum):
    Wished = 0
    Ordered = 1
    Owned = 2
    Favorites = 3
