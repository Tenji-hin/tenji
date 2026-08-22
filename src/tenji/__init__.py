"""Asynchronous Python client for scraping data from MyFigureCollection (MFC)."""

from importlib.metadata import PackageNotFoundError, version as _get_version

from .client import MFCException, MfcClient
from .exceptions import ParserException, RequestException
from .mfc_response import MFCResponse
from .model.category import ItemCategory
from .model.item.item import Character, Company, Item
from .model.item.partner_listing import PartnerListing
from .model.item.partner_status import PartnerListingStatus
from .model.meta import Meta
from .model.paginated import Pagination
from .model.shop.shop import Shop
from .model.shop.shop_category import ShopCategory
from .model.shop.shop_list_item import ShopListItem
from .model.user.collection import Collection, CollectionStats
from .model.user.collectionstatus import CollectionStatus
from .model.user.profile import About, Profile
from .model.user.user_list import UserList
from .model.user.user_list_item import UserListItem
from .model.user.users_lists import UserLists

try:
    __version__ = _get_version("tenji")
except PackageNotFoundError:  # running from a source checkout
    __version__ = "0.0.0.dev0"

__all__ = [
    "__version__",
    # client
    "MfcClient",
    # exceptions
    "MFCException",
    "ParserException",
    "RequestException",
    # responses
    "MFCResponse",
    # items
    "Character",
    "Company",
    "Item",
    "ItemCategory",
    "PartnerListing",
    "PartnerListingStatus",
    # shops
    "Shop",
    "ShopCategory",
    "ShopListItem",
    # users
    "About",
    "Collection",
    "CollectionStats",
    "CollectionStatus",
    "Profile",
    "UserList",
    "UserListItem",
    "UserLists",
    # shared
    "Meta",
    "Pagination",
]
