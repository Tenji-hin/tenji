import datetime

import pytest

from tenji.model.category import ItemCategory
from tenji.parser.user.collection import CollectionParser
from tenji.parser.user.profile import ProfileParser
from tenji.parser.user.user_list import UserListParser
from tenji.parser.user.user_lists import UserListsParser

UTC = datetime.timezone.utc


class TestCollectionParser:
    @pytest.fixture
    def collection(self, mfc_response):
        return CollectionParser(mfc_response("collection.html")).parse()

    def test_stats(self, collection):
        assert collection.stats.owned == 128
        assert collection.stats.ordered == 7
        assert collection.stats.wished == 42

    def test_items(self, collection):
        assert [item.id for item in collection.items] == [198579, 312044, 885511]
        assert [item.name for item in collection.items] == [
            "Hatsune Miku",
            "Nendoroid Rin",
            "Miku Art Book",
        ]
        assert (
            collection.items[0].thumbnail
            == "https://static.myfigurecollection.net/upload/items/0/198579-4200e.jpg"
        )

    def test_categories_come_from_the_stamp_class(self, collection):
        assert [item.category for item in collection.items] == [
            ItemCategory.Prepainted,
            ItemCategory.Trading,
            ItemCategory.Books,
        ]

    def test_pagination(self, collection):
        assert collection.pagination.current_page == 2
        assert collection.pagination.total_pages == 5
        assert collection.pagination.total_items == 177
        assert collection.pagination.has_next_page is True

    def test_single_page_collection(self, mfc_response):
        collection = CollectionParser(
            mfc_response("collection_single_page.html")
        ).parse()
        assert len(collection.items) == 2
        assert collection.pagination.current_page == 1
        assert collection.pagination.has_next_page is False
        assert collection.pagination.total_pages == 1


class TestProfileParser:
    @pytest.fixture
    def profile(self, mfc_response):
        return ProfileParser(mfc_response("profile.html")).parse()

    def test_headline(self, profile):
        assert profile.username == "tester"
        assert profile.subtitle == "Figure Collector"
        assert profile.status == "Currently hunting for Miku figures"

    def test_images(self, profile):
        assert (
            profile.banner
            == "https://static.myfigurecollection.net/upload/banners/0/42-abcde.jpg"
        )
        assert (
            profile.avatar
            == "https://static.myfigurecollection.net/upload/users/0/42-9c8e7.jpg"
        )

    def test_stats(self, profile):
        assert profile.last_visit == datetime.datetime(2017, 12, 21, 13, 1, 50, tzinfo=UTC)
        assert profile.joined == datetime.datetime(2011, 3, 4, 9, 15, 0, tzinfo=UTC)
        assert profile.hits == 1234
        assert profile.placement == 42

    def test_about(self, profile):
        about = profile.about
        assert about.level == 57
        assert about.gender == "Male"
        assert about.age == "31"
        assert about.location == "Ohio, USA"
        assert about.occupation == "Software Developer"
        assert about.homepage == "https://example.com/"
        assert about.shows == "Cowboy Bebop"
        assert about.books == "Berserk"
        assert about.games == "Persona 5"
        assert about.moe_points == "Twintails"

    def test_optional_about_fields_are_none_when_absent(self, mfc_response):
        profile = ProfileParser(mfc_response("profile_minimal.html")).parse()
        assert profile.username == "newbie"
        assert profile.subtitle is None
        assert profile.status is None
        assert profile.about.level == 1
        assert profile.about.gender is None
        assert profile.about.location is None
        assert profile.about.homepage is None

    def test_unparseable_last_visit_falls_back_to_now(self, mfc_response):
        before = datetime.datetime.now(UTC)
        profile = ProfileParser(mfc_response("profile_minimal.html")).parse()
        after = datetime.datetime.now(UTC)
        # the fallback is timezone-aware, matching successfully parsed values
        assert profile.last_visit.tzinfo is not None
        assert before <= profile.last_visit <= after


class TestUserListParser:
    @pytest.fixture
    def user_list(self, mfc_response):
        return UserListParser(mfc_response("user_list.html")).parse()

    def test_basic_fields(self, user_list):
        assert user_list.id == 1234
        assert user_list.name == "Favourite Mikus"
        assert user_list.owner == "tester"
        assert (
            user_list.icon
            == "https://static.myfigurecollection.net/pics/list-1234.png"
        )
        assert user_list.created == datetime.datetime(2017, 12, 21, 13, 1, 50, tzinfo=UTC)

    def test_description_keeps_inline_markup(self, user_list):
        assert user_list.description == "A list of <b>great</b> figures."

    def test_items(self, user_list):
        assert [item.id for item in user_list.items] == [198579, 885511]
        assert [item.name for item in user_list.items] == [
            "Hatsune Miku",
            "Miku Art Book",
        ]
        assert [item.category for item in user_list.items] == [
            ItemCategory.Prepainted,
            ItemCategory.Books,
        ]

    def test_tags(self, user_list):
        assert user_list.tags == ["miku", "vocaloid"]

    def test_pagination(self, user_list):
        assert user_list.pagination.total_items == 2
        assert user_list.pagination.has_next_page is False


class TestUserListsParser:
    @pytest.fixture
    def lists(self, mfc_response):
        return UserListsParser(mfc_response("user_lists.html")).parse()

    def test_items(self, lists):
        assert [item.id for item in lists.items] == [1234, 5678]
        assert [item.name for item in lists.items] == [
            "Favourite Mikus",
            "Wishlist 2024",
        ]
        assert [item.owner for item in lists.items] == ["tester", "tester"]
        assert (
            lists.items[0].icon
            == "https://static.myfigurecollection.net/pics/list-1234.png"
        )

    def test_creation_dates(self, lists):
        assert lists.items[0].created == datetime.datetime(
            2017, 12, 21, 13, 1, 50, tzinfo=UTC
        )
        assert lists.items[1].created == datetime.datetime(
            2024, 1, 2, 8, 30, 0, tzinfo=UTC
        )

    def test_item_counts_are_parsed_without_separators(self, lists):
        assert [item.count for item in lists.items] == [42, 1003]

    def test_pagination(self, lists):
        assert lists.pagination.total_items == 2
        assert lists.pagination.current_page == 1
