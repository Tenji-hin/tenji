import pytest

from tenji.model.category import ItemCategory
from tenji.parser.item.item import ItemParser


@pytest.fixture
def item(mfc_response):
    return ItemParser(mfc_response("item.html")).parse()


class TestItemParser:
    def test_basic_fields(self, item):
        assert item.id == 198579
        assert item.name == "Hatsune Miku 1/8 Scale Figure"
        assert (
            item.thumbnail
            == "https://static.myfigurecollection.net/upload/items/0/198579-4200e.jpg"
        )

    def test_category(self, item):
        assert item.category is ItemCategory.Prepainted

    def test_characters(self, item):
        assert [c.name for c in item.characters] == ["Hatsune Miku", "Kagamine Rin"]
        assert [c.id for c in item.characters] == [12345, 67890]
        assert (
            item.characters[0].avatar
            == "https://static.myfigurecollection.net/upload/entries/0/12345.jpg"
        )

    def test_plural_character_label_is_not_matched_twice(self, item):
        # "Character" is a substring of "Characters", so a naive lookup over both
        # labels collects the same links twice.
        assert len(item.characters) == 2

    def test_companies(self, item):
        assert [c.name for c in item.companies] == [
            "Good Smile Company",
            "Crypton Future Media",
        ]
        assert [c.id for c in item.companies] == [1111, 2222]
        assert [c.role for c in item.companies] == ["Manufacturer", "Copyright"]
        assert (
            item.companies[0].logo
            == "https://static.myfigurecollection.net/upload/entries/0/1111.jpg"
        )


class TestItemFieldLookup:
    def test_missing_field_container_returns_none(self, mfc_response):
        parser = ItemParser(mfc_response("item.html"))
        assert parser.get_item_field_container("Artist") is None

    def test_missing_labels_yield_no_fields(self, mfc_response):
        parser = ItemParser(mfc_response("item.html"))
        assert parser.try_get_item_fields(["Artist", "Artists"]) == []

    def test_singular_label_matches_the_plural_container(self, mfc_response):
        parser = ItemParser(mfc_response("item.html"))
        container = parser.get_item_field_container("Character")
        assert container is not None
        assert len(container.select("a")) == 2
