import datetime

import pytest
from pydantic import ValidationError

from tenji.model.category import ItemCategory, get_item_category_from_str
from tenji.model.item.item import Character, Company, Item
from tenji.model.item.partner_status import PartnerListingStatus
from tenji.model.paginated import Pagination
from tenji.model.shop.shop_category import ShopCategory
from tenji.model.user.collection import Collection, CollectionStats
from tenji.model.user.collectionstatus import CollectionStatus
from tenji.model.user.user_list import UserList

CATEGORY_LABELS = {
    "Prepainted": ItemCategory.Prepainted,
    "Action/Dolls": ItemCategory.ActionDolls,
    "Trading": ItemCategory.Trading,
    "Garage Kits": ItemCategory.GarageKits,
    "Model Kits": ItemCategory.ModelKits,
    "Plushes": ItemCategory.Plushes,
    "Accessories": ItemCategory.Accessories,
    "Linens": ItemCategory.Linens,
    "Dishes": ItemCategory.Dishes,
    "Hanged up": ItemCategory.HangedUp,
    "Apparel": ItemCategory.Apparel,
    "On Walls": ItemCategory.OnWalls,
    "Stationeries": ItemCategory.Stationeries,
    "Misc": ItemCategory.Misc,
    "Books": ItemCategory.Books,
    "Music": ItemCategory.Music,
    "Video": ItemCategory.Video,
    "Games": ItemCategory.Games,
    "Software": ItemCategory.Software,
}


class TestItemCategory:
    @pytest.mark.parametrize("label,expected", sorted(CATEGORY_LABELS.items()))
    def test_maps_labels_to_categories(self, label, expected):
        assert get_item_category_from_str(label) == expected

    @pytest.mark.parametrize("label", ["", "prepainted", "Unknown", "Figures"])
    def test_raises_for_unknown_labels(self, label):
        with pytest.raises(ValueError, match="Unknown MFC item category"):
            get_item_category_from_str(label)

    def test_the_unknown_label_is_named_in_the_error(self):
        with pytest.raises(ValueError, match="Figurines"):
            get_item_category_from_str("Figurines")

    @pytest.mark.parametrize("label", [None, 1, []])
    def test_raises_for_non_string_input(self, label):
        with pytest.raises(ValueError, match="must be a string"):
            get_item_category_from_str(label)

    def test_surrounding_whitespace_is_ignored(self):
        assert get_item_category_from_str("  Prepainted\n") is ItemCategory.Prepainted

    def test_every_category_has_a_label(self):
        assert set(ItemCategory) == set(CATEGORY_LABELS.values())


class TestCollectionStatus:
    @pytest.mark.parametrize(
        "status,value",
        [
            (CollectionStatus.Wished, "0"),
            (CollectionStatus.Ordered, "1"),
            (CollectionStatus.Owned, "2"),
            (CollectionStatus.Favorites, "3"),
        ],
    )
    def test_values(self, status, value):
        assert status.value == value


class TestShopCategory:
    def test_values(self):
        assert ShopCategory.WebShop == 1
        assert ShopCategory.LocalShop == 2
        assert ShopCategory.Proxy == 3
        assert ShopCategory.EbayShop == 4


class TestPartnerListingStatus:
    @pytest.mark.parametrize(
        "text", ["Available", "Maybe available", "Not available"]
    )
    def test_built_from_the_availability_text(self, text):
        assert str(PartnerListingStatus(text)) == text

    def test_unknown_availability_raises(self):
        with pytest.raises(ValueError):
            PartnerListingStatus("Sold out")


class TestItem:
    def test_defaults(self):
        item = Item(id=1, name=None, thumbnail=None, category=ItemCategory.Books)
        assert item.characters == []
        assert item.companies == []

    def test_category_is_coerced_from_an_int(self):
        item = Item(id=1, name="n", thumbnail="t", category=21)
        assert item.category is ItemCategory.Books

    def test_id_is_required(self):
        with pytest.raises(ValidationError):
            Item(name="n", thumbnail="t", category=ItemCategory.Books)

    def test_nested_models(self):
        item = Item(
            id=1,
            name="n",
            thumbnail="t",
            category=ItemCategory.Prepainted,
            characters=[Character(id=2, name="Miku", avatar="a.jpg")],
            companies=[Company(id=3, name="GSC", logo="l.jpg", role="Manufacturer")],
        )
        assert item.characters[0].name == "Miku"
        assert item.companies[0].role == "Manufacturer"


class TestPagination:
    def test_coerces_string_page_counts(self):
        pagination = Pagination(
            current_page=2, has_next_page=True, total_pages="5", total_items=177
        )
        assert pagination.total_pages == 5

    def test_all_fields_are_required(self):
        with pytest.raises(ValidationError):
            Pagination(current_page=1, has_next_page=False, total_pages=1)


class TestCollection:
    def test_defaults(self):
        collection = Collection()
        assert collection.items == []
        assert collection.stats is None
        assert collection.pagination is None

    def test_stats_default_to_zero(self):
        assert CollectionStats() == CollectionStats(owned=0, ordered=0, wished=0)


class TestUserList:
    def test_optional_fields_default(self):
        created = datetime.datetime(2017, 12, 21, tzinfo=datetime.timezone.utc)
        user_list = UserList(
            id=1, name="n", owner="o", icon="i.png", created=created
        )
        assert user_list.description is None
        assert user_list.items == []
        assert user_list.tags == []
        assert user_list.pagination is None
